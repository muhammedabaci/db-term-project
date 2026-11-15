from backend.db_connection import get_connection


def get_frequencies_by_airport(airport_ref):
    """Returns all frequencies of one airport."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, airport_ref, airport_ident, type, description, frequency_mhz
            FROM airport_frequencies
            WHERE airport_ref = %s
            ORDER BY type
            """,
            (airport_ref,),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Hata (get_frequencies_by_airport): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_frequency(freq_id, airport_ref, airport_ident, freq_type,
                     description, frequency_mhz):
    """Inserts one frequency row. Returns True on success."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO airport_frequencies
                (id, airport_ref, airport_ident, type, description, frequency_mhz)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (freq_id, airport_ref, airport_ident, freq_type,
             description, frequency_mhz),
        )
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Hata (insert_frequency): {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()