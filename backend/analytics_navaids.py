"""Analytical queries for navigation aids (navaids)."""

from backend.db_connection import get_connection


def get_navaids_by_country(country_code):
    """Return navaids for a country with their optional associated airport.

    Each result contains the navaid name and type, plus the full airport name
    when ``associated_airport`` points to an airport in the database.
    """
    conn = get_connection()
    if conn is None:
        return []

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT n.name AS navaid_name,
                   n.type AS navaid_type,
                   a.name AS airport_name
            FROM navaids AS n
            JOIN countries AS c
              ON c.code = n.iso_country
            LEFT JOIN airports AS a
              ON a.ident = n.associated_airport
            WHERE c.code = %s
            ORDER BY n.name, n.ident;
            """,
            (country_code,),
        )
        return cursor.fetchall()
    except Exception as error:
        print(f"Navaid country report failed: {error}")
        return []
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()


def get_navaid_type_counts_over(minimum_count=100):
    """Return navaid types occurring more than ``minimum_count`` times.

    Results are ordered from the least common qualifying type to the most
    common. ``minimum_count`` is bound as a query parameter.
    """
    conn = get_connection()
    if conn is None:
        return []

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT type AS navaid_type,
                   COUNT(*) AS navaid_count
            FROM navaids
            WHERE type IS NOT NULL
            GROUP BY type
            HAVING COUNT(*) > %s
            ORDER BY navaid_count ASC, navaid_type ASC;
            """,
            (minimum_count,),
        )
        return cursor.fetchall()
    except Exception as error:
        print(f"Navaid type report failed: {error}")
        return []
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()
