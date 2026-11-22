import os
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

import psycopg2

from backend import analytics_runways
from backend.db_connection import get_connection


@unittest.skipUnless(os.environ.get("RUN_DB_TESTS") == "1", "Requires local PostgreSQL")
class RunwayAnalyticsDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection()
        self.assertIsNotNone(self.conn, "Start the project's PostgreSQL container first")
        self.addCleanup(self.conn.close)
        # Temporary tables shadow production tables only on this test connection.
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TEMP TABLE regions (code TEXT, name TEXT);
                CREATE TEMP TABLE airports (id INT, name TEXT, iso_region TEXT);
                CREATE TEMP TABLE runways (
                    id INT, airport_ref INT, surface TEXT, length_ft INT, lighted INT
                );
                INSERT INTO regions VALUES ('TR-34', 'Istanbul');
                INSERT INTO airports VALUES (1, 'Test Airport', 'TR-34');
            """)
        self.connection_patch = patch.object(analytics_runways, "get_connection", return_value=self.conn)
        self.connection_patch.start()
        self.addCleanup(self.connection_patch.stop)

    def test_lit_runways_join_names_and_use_strict_length_boundary(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO runways VALUES
                    (1, 1, 'ASPH', 10001, 1),
                    (2, 1, 'CONC', 10000, 1),
                    (3, 1, 'GRS', 12000, 0),
                    (4, 1, 'CONC', 11000, 1),
                    (5, 1, 'ASPH', NULL, 1);
            """)
        self.assertEqual(
            analytics_runways.get_lighted_runways(10000),
            [(4, 'Test Airport', 'Istanbul', 'CONC', 11000),
             (1, 'Test Airport', 'Istanbul', 'ASPH', 10001)],
        )
        self.assertTrue(self.conn.closed)

    def test_surface_counts_exclude_exactly_1000_and_sort_descending(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO runways (id, surface)
                    SELECT n, 'ASPH' FROM generate_series(1, 1001) n;
                INSERT INTO runways (id, surface)
                    SELECT n + 2000, 'CONC' FROM generate_series(1, 1000) n;
                INSERT INTO runways (id, surface)
                    SELECT n + 4000, 'GRS' FROM generate_series(1, 1002) n;
            """)
        self.assertEqual(
            analytics_runways.get_surfaces_with_many_runways(),
            [('GRS', 1002), ('ASPH', 1001)],
        )
        self.assertTrue(self.conn.closed)

    def test_empty_reports(self):
        self.assertEqual(analytics_runways.get_lighted_runways(10000), [])

    def test_custom_surface_threshold(self):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO runways (id, surface) VALUES (1, 'ASPH'), (2, 'ASPH'), (3, 'GRS')")
        self.assertEqual(analytics_runways.get_surfaces_with_many_runways(1), [('ASPH', 2)])


class RunwayAnalyticsFailureTests(unittest.TestCase):
    def test_unavailable_connection_returns_empty_reports(self):
        with patch.object(analytics_runways, "get_connection", return_value=None):
            self.assertEqual(analytics_runways.get_lighted_runways(10000), [])
            self.assertEqual(analytics_runways.get_surfaces_with_many_runways(), [])

    def test_database_errors_return_empty_reports_and_release_resources(self):
        for function, args in [
            (analytics_runways.get_lighted_runways, (10000,)),
            (analytics_runways.get_surfaces_with_many_runways, ()),
        ]:
            for failure in ("cursor", "execute", "fetchall"):
                with self.subTest(function=function.__name__, failure=failure):
                    conn = Mock()
                    cursor = conn.cursor.return_value
                    target = conn.cursor if failure == "cursor" else getattr(cursor, failure)
                    target.side_effect = psycopg2.Error("test database error")
                    with patch.object(analytics_runways, "get_connection", return_value=conn), redirect_stdout(StringIO()):
                        self.assertEqual(function(*args), [])
                    conn.close.assert_called_once()
                    if failure != "cursor":
                        cursor.close.assert_called_once()

    def test_external_values_are_bound_as_parameters(self):
        value = "0; DROP TABLE runways; --"
        for function in (analytics_runways.get_lighted_runways,
                         analytics_runways.get_surfaces_with_many_runways):
            with self.subTest(function=function.__name__):
                conn = Mock()
                conn.cursor.return_value.fetchall.return_value = []
                with patch.object(analytics_runways, "get_connection", return_value=conn):
                    function(value)
                query, params = conn.cursor.return_value.execute.call_args.args
                self.assertNotIn(value, query)
                self.assertEqual(params, (value,))


if __name__ == "__main__":
    unittest.main()
