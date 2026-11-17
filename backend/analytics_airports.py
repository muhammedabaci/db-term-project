import psycopg2
from backend.db_connection import get_connection

def get_airport_location_details(airport_ident: str):
    """
    SENARYO 1: Derin JOIN
    Belirtilen havalimanı koduna (ident) göre havalimanının adını, tipini, 
    bulunduğu ülkeyi ve bölgeyi tek bir satır olarak getirir.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        
        # Dışarıdan gelen airport_ident değişkenini %s ile güvenle içeri alıyoruz
        query = """
            SELECT 
                a.name AS airport_name, 
                a.type AS airport_type, 
                c.name AS country_name, 
                r.name AS region_name
            FROM airports a
            INNER JOIN countries c ON a.iso_country = c.code
            INNER JOIN regions r ON a.iso_region = r.code
            WHERE a.ident = %s;
        """
        cursor.execute(query, (airport_ident,))
        return cursor.fetchone()  # Tek bir havalimanı döneceği için fetchone()
        
    except psycopg2.Error as e:
        print(f"❌ Lokasyon detayı çekilirken hata oluştu: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_countries_with_many_airports(min_airport_count: int = 50):
    """
    SENARYO 2: GROUP BY ve HAVING
    Belirtilen sayıdan daha fazla havalimanına sahip ülkeleri ve 
    havalimanı sayılarını çoktan aza doğru sıralayarak listeler.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        
        # HAVING filtresindeki eşik değeri %s ile dinamik hale getiriyoruz
        query = """
            SELECT 
                c.name AS country_name, 
                COUNT(a.id) AS total_airports
            FROM countries c
            INNER JOIN airports a ON c.code = a.iso_country
            GROUP BY c.name
            HAVING COUNT(a.id) > %s
            ORDER BY total_airports DESC;
        """
        cursor.execute(query, (min_airport_count,))
        return cursor.fetchall()  # Birden fazla ülke döneceği için fetchall()
        
    except psycopg2.Error as e:
        print(f"❌ Ülke istatistikleri çekilirken hata oluştu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Dosya doğrudan çalıştırıldığında test işlemleri yapar
if __name__ == "__main__":
    print("--- 🌍 SENARYO 1: Lokasyon Haritası (LTFM) ---")
    ltfm_info = get_airport_location_details("LTFM")
    if ltfm_info:
        # Tuple içindeki verilere index ile erişiyoruz: (name, type, country, region)
        print(f"Havalimanı : {ltfm_info[0]} ({ltfm_info[1]})")
        print(f"Konum      : {ltfm_info[3]}, {ltfm_info[2]}")
    else:
        print("Havalimanı bulunamadı.")

    print("\n--- 📊 SENARYO 2: Yoğunluk Raporu (>50 Havalimanı) ---")
    countries_stats = get_countries_with_many_airports(50)
    
    if countries_stats:
        print(f"Kriteri sağlayan toplam ülke sayısı: {len(countries_stats)}")
        print("-" * 45)
        # Sadece en yoğun ilk 10 ülkeyi ekrana basalım
        for row in countries_stats[:10]: 
            print(f"Ülke: {row[0]:<25} | Havalimanı Sayısı: {row[1]}")
    else:
        print("Kriteri sağlayan ülke bulunamadı.")