from backend.db_connection import get_connection


def get_airports_by_frequency_type(freq_type, limit=100):
    """
    Returns (airport_name, frequency_mhz, country_name) rows for
    airports that have a frequency of the given type (e.g. 'TWR').
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT a.name AS airport_name,
                   f.frequency_mhz,
                   c.name AS country_name
            FROM airport_frequencies f
            JOIN airports a  ON f.airport_ref = a.id
            JOIN countries c ON a.iso_country = c.code
            WHERE f.type = %s
            ORDER BY c.name, a.name
            LIMIT %s
            """,
            (freq_type.upper(), limit),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Hata (get_airports_by_frequency_type): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_frequency_types_over_threshold(min_count=500):
    """
    Groups all frequencies by type and returns (type, total) rows for
    types with more than min_count records, largest first.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT type, COUNT(*) AS total
            FROM airport_frequencies
            GROUP BY type
            HAVING COUNT(*) > %s
            ORDER BY total DESC
            """,
            (min_count,),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Hata (get_frequency_types_over_threshold): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
