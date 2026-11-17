"""Database operations for the navaids table."""

from backend.db_connection import get_connection


def get_navaid_by_id(navaid_id):
    """Return a navaid row by its primary key, or None if it is unavailable."""
    conn = get_connection()
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, ident, name, type, frequency_khz,
                   iso_country, power, associated_airport
            FROM navaids
            WHERE id = %s;
            """,
            (navaid_id,),
        )
        return cursor.fetchone()
    except Exception as error:
        print(f"Navaid lookup failed: {error}")
        return None
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()


def insert_basic_navaid(
    navaid_id,
    ident,
    name,
    navaid_type,
    frequency_khz=None,
    iso_country=None,
    power=None,
    associated_airport=None,
):
    """Insert a basic navaid record; return True on success and False on error."""
    conn = get_connection()
    if conn is None:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO navaids
                (id, ident, name, type, frequency_khz,
                 iso_country, power, associated_airport)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                navaid_id,
                ident,
                name,
                navaid_type,
                frequency_khz,
                _empty_to_none(iso_country),
                _empty_to_none(power),
                _empty_to_none(associated_airport),
            ),
        )
        conn.commit()
        return True
    except Exception as error:
        print(f"Navaid insert failed: {error}")
        try:
            conn.rollback()
        except Exception as rollback_error:
            print(f"Navaid insert rollback failed: {rollback_error}")
        return False
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()


def _empty_to_none(value):
    """Map blank optional text fields to SQL NULL."""
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value
