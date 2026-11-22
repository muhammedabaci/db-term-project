"""8. hafta: pistler için JOIN ve GROUP BY / HAVING raporları."""

import psycopg2

from backend.db_connection import get_connection


def get_lighted_runways(min_length_ft: int):
    """Uzunluğu eşiği aşan aydınlatmalı pistleri uzunluk azalan sırada getirir.

    Satır biçimi: (runway_id, airport_name, region_name, surface, length_ft).
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
            SELECT rw.id AS runway_id,
                   a.name AS airport_name,
                   r.name AS region_name,
                   rw.surface,
                   rw.length_ft
            FROM runways rw
            INNER JOIN airports a ON rw.airport_ref = a.id
            INNER JOIN regions r ON a.iso_region = r.code
            WHERE rw.length_ft > %s AND rw.lighted = 1
            ORDER BY rw.length_ft DESC, rw.id;
        """
        cursor.execute(query, (min_length_ft,))
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Aydınlatmalı pist raporu getirilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_surfaces_with_many_runways(min_runway_count: int = 1000):
    """Eşikten fazla pisti olan yüzeyleri (surface, total_runways) olarak getirir.

    Sayılar çoktan aza sıralanır; yüzey değerleri veritabanındaki haliyle gruplanır.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
            SELECT surface, COUNT(*) AS total_runways
            FROM runways
            GROUP BY surface
            HAVING COUNT(*) > %s
            ORDER BY total_runways DESC, surface;
        """
        cursor.execute(query, (min_runway_count,))
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Pist yüzey istatistikleri getirilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print("--- 10000 Feet Üzerindeki Aydınlatmalı Pistler (İlk 10) ---")
    for row in get_lighted_runways(10000)[:10]:
        print(row)

    print("\n--- Dünya Genelinde 1000'den Fazla Pisti Olan Yüzey Tipleri ---")
    for surface, count in get_surfaces_with_many_runways():
        print(f"Yüzey: {surface} | Pist sayısı: {count}")
