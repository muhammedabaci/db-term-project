# backend/regions_manager.py

from backend.db_connection import get_connection


def get_regions_by_country(country_code):
    """
    Verilen ülke koduna (ör. 'TR') bağlı tüm bölgeleri bölge koduna göre sıralı getirir.
    Her satır: (id, code, local_code, name, continent, iso_country)
    Bölge yoksa boş liste, hata olursa None döner.
    """
    conn = get_connection()
    if not conn:
        return None

    cursor = None
    try:
        cursor = conn.cursor()

        # DİKKAT: %s ile parametrik sorgu yazıyoruz (SQL Injection koruması).
        query = """
            SELECT id, code, local_code, name, continent, iso_country
            FROM regions
            WHERE iso_country = %s
            ORDER BY code;
        """

        cursor.execute(query, (country_code,))
        return cursor.fetchall()  # Bir ülkenin birden fazla bölgesi olabilir

    except Exception as e:
        print(f"❌ Bölgeler çekilirken hata oluştu: {e}")
        return None

    finally:
        # Veritabanı kaynaklarını her durumda serbest bırak
        if cursor:
            cursor.close()
        conn.close()


def insert_region(region_id, code, local_code, name, continent, iso_country,
                  wikipedia_link=None, keywords=None):
    """
    regions tablosuna yeni bir bölge ekler (Temel CRUD - INSERT).
    iso_country, countries tablosunda var olan bir ülke kodu olmalıdır (fk_regions_country).
    wikipedia_link ve keywords verilmezse NULL olarak kaydedilir.
    Başarılıysa True, hata olursa False döner.
    """
    conn = get_connection()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO regions (id, code, local_code, name, continent, iso_country,
                                 wikipedia_link, keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        cursor.execute(query, (region_id, code, local_code, name, continent, iso_country,
                               wikipedia_link, keywords))

        # INSERT'in veritabanına kalıcı olarak yazılması için commit şart
        conn.commit()
        print(f"✅ {name} ({code}) başarıyla veritabanına eklendi.")
        return True

    except Exception as e:
        print(f"❌ Bölge eklenirken hata: {e}")
        # Hata durumunda (ör. ülke kodu countries tablosunda yoksa) işlemi geri al
        conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()


# Dosya doğrudan çalıştırıldığında test işlemleri yapar:
#   python -m backend.regions_manager
if __name__ == "__main__":
    print("--- 🗺️ Bölge Yöneticisi Testi Başlıyor ---")

    # 1. SELECT Testi: Türkiye'ye bağlı bölgeleri getirelim
    print("\n[TEST 1] TR ülkesine bağlı bölgeler aranıyor")
    tr_regions = get_regions_by_country("TR")
    if tr_regions:
        print(f"Bulunan bölge sayısı: {len(tr_regions)}")
        for region in tr_regions[:3]:
            print(f"  ID={region[0]}, Kod={region[1]}, İsim={region[3]}")
    else:
        print("TR'ye bağlı bölge bulunamadı (veriler yüklenmemiş olabilir).")

    # 2. INSERT Testi: Türkiye'ye bağlı hayali bir test bölgesi ekleyelim
    # (Test ikinci kez çalıştırılırsa bu id/code zaten var olacağı için
    #  hata verip rollback yapar; bu beklenen davranıştır.)
    print("\n[TEST 2] Yeni bölge ekleniyor: TR-TEST")
    insert_region(
        region_id=999999,
        code="TR-TEST",
        local_code="TEST",
        name="Test Bölgesi",
        continent="AS",
        iso_country="TR",
    )

    # 3. Negatif Test: Var olmayan bir ülkeye (QQ) bağlı bölge
    # fk_regions_country kısıtı bunu reddetmeli; fonksiyon rollback yapıp False dönmeli.
    print("\n[TEST 3] Var olmayan ülkeye (QQ) bölge eklenmeye çalışılıyor")
    insert_region(
        region_id=999998,
        code="QQ-TEST",
        local_code="TEST",
        name="Geçersiz Test Bölgesi",
        continent="EU",
        iso_country="QQ",
    )
