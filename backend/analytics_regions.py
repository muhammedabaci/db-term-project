import psycopg2
from backend.db_connection import get_connection


def get_regions_by_continent(continent_code: str):
    """
    SENARYO 1: Derin JOIN
    Belirtilen kıta koduna (örn. 'EU') göre, o kıtadaki bölgelerin/eyaletlerin
    tam adını ve bağlı oldukları ülkenin tam adını getirir.
    Her satır: (region_code, region_name, country_name)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()

        # Dışarıdan gelen continent_code değişkenini %s ile güvenle içeri alıyoruz
        query = """
            SELECT
                r.code AS region_code,
                r.name AS region_name,
                c.name AS country_name
            FROM regions r
            INNER JOIN countries c ON r.iso_country = c.code
            WHERE r.continent = %s
            ORDER BY c.name, r.name;
        """
        cursor.execute(query, (continent_code,))
        return cursor.fetchall()  # Bir kıtada çok sayıda bölge olacağı için fetchall()

    except psycopg2.Error as e:
        print(f"❌ Kıtadaki bölgeler çekilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_regions_with_many_airports(min_airport_count: int = 100):
    """
    SENARYO 2: GROUP BY ve HAVING
    Sınırları içinde belirtilen sayıdan fazla havalimanı bulunan büyük bölgeleri/eyaletleri,
    bağlı oldukları ülkeyle birlikte, havalimanı sayısına göre çoktan aza sıralar.
    Her satır: (region_code, region_name, country_name, total_airports)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()

        # DİKKAT: Gruplamayı bölge adına göre değil, benzersiz bölge koduna (r.code) göre yapıyoruz.
        # Bölge adları benzersiz değil: örneğin 63 farklı ülkede "(unassigned)" adlı bölge var.
        # Sadece ada göre gruplasaydık bu bölgelerin havalimanları tek satırda toplanırdı.
        # HAVING filtresindeki eşik değeri %s ile dinamik hale getiriyoruz.
        query = """
            SELECT
                r.code AS region_code,
                r.name AS region_name,
                c.name AS country_name,
                COUNT(a.id) AS total_airports
            FROM regions r
            INNER JOIN countries c ON r.iso_country = c.code
            INNER JOIN airports a ON a.iso_region = r.code
            GROUP BY r.code, r.name, c.name
            HAVING COUNT(a.id) > %s
            ORDER BY total_airports DESC, r.code;
        """
        cursor.execute(query, (min_airport_count,))
        return cursor.fetchall()  # Birden fazla bölge döneceği için fetchall()

    except psycopg2.Error as e:
        print(f"❌ Bölge istatistikleri çekilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Dosya doğrudan çalıştırıldığında test işlemleri yapar:
#   python -m backend.analytics_regions
if __name__ == "__main__":
    print("--- 🌍 SENARYO 1: Avrupa'daki Bölgeler (EU) ---")
    eu_regions = get_regions_by_continent("EU")
    if eu_regions:
        print(f"Bulunan bölge sayısı: {len(eu_regions)}")
        print("-" * 60)
        # Sadece ilk 10 bölgeyi ekrana basalım: (region_code, region_name, country_name)
        for row in eu_regions[:10]:
            print(f"Bölge: {row[1]:<30} | Ülke: {row[2]}")
    else:
        print("Bu kıtada bölge bulunamadı.")

    # SQL Injection denemesi: %s kullandığımız için bu metin komut olarak değil,
    # sıradan bir kıta kodu olarak aranır ve hiçbir sonuç dönmez.
    print("\n--- 🛡️ SQL Injection Denemesi ---")
    injection_test = get_regions_by_continent("EU' OR '1'='1")
    print(f"Dönen satır sayısı: {len(injection_test)} (0 olmalı)")

    print("\n--- 📊 SENARYO 2: Büyük Bölgeler (>100 Havalimanı) ---")
    big_regions = get_regions_with_many_airports(100)
    if big_regions:
        print(f"Kriteri sağlayan toplam bölge sayısı: {len(big_regions)}")
        print("-" * 60)
        # Sadece en yoğun ilk 10 bölgeyi ekrana basalım
        for row in big_regions[:10]:
            print(f"Bölge: {row[1]:<20} | Ülke: {row[2]:<20} | Havalimanı Sayısı: {row[3]}")
    else:
        print("Kriteri sağlayan bölge bulunamadı.")
