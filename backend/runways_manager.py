import psycopg2
from backend.db_connection import get_connection


def get_runways(limit: int = 10):
    """Belirtilen sayıda pist (runway) kaydını getirir."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
            SELECT id, airport_ref, airport_ident, length_ft, width_ft,
                   surface, lighted, closed, le_ident, he_ident
            FROM runways
            ORDER BY id
            LIMIT %s;
        """
        cursor.execute(query, (limit,))
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Pistler getirilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_runways_by_airport(airport_ref: int):
    """Belirli bir havalimanına (airport_ref) ait tüm pistleri getirir."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
            SELECT id, airport_ref, airport_ident, length_ft, width_ft,
                   surface, lighted, closed, le_ident, he_ident
            FROM runways
            WHERE airport_ref = %s
            ORDER BY id;
        """
        cursor.execute(query, (airport_ref,))
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Havalimanı pistleri getirilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def add_runway(
    runway_id: int,
    airport_ref: int,
    airport_ident: str,
    length_ft: int,
    width_ft: int,
    surface: str,
    lighted: int = 0,
    closed: int = 0,
    le_ident: str = None,
    he_ident: str = None,
) -> bool:
    """runways tablosuna yeni bir pist kaydı ekler."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        query = """
            INSERT INTO runways (
                id, airport_ref, airport_ident, length_ft, width_ft,
                surface, lighted, closed, le_ident, he_ident
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            query,
            (
                runway_id,
                airport_ref,
                airport_ident,
                length_ft,
                width_ft,
                surface,
                lighted,
                closed,
                le_ident,
                he_ident,
            ),
        )
        conn.commit()
        print(f"✅ Pist başarıyla eklendi (id={runway_id}, airport_ident={airport_ident}).")
        return True
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"❌ Pist eklenemedi (rollback yapıldı): {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print("--- İlk 5 Pist ---")
    for row in get_runways(limit=5):
        print(row)

    print("\n--- 6523 ID'li Havalimanının Pistleri ---")
    for row in get_runways_by_airport(6523):
        print(row)
