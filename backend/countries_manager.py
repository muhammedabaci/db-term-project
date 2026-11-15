# backend/countries_manager.py

from backend.db_connection import get_connection


def get_country_by_code(country_code):
    """
    İki harfli ülke koduna (ör. 'TR') sahip ülkenin bilgilerini getirir.
    Dönen satır: (id, code, name, continent, wikipedia_link, keywords)
    Kayıt yoksa veya hata olursa None döner.
    """
    conn = get_connection()
    if not conn:
        return None

    cursor = None
    try:
        cursor = conn.cursor()

        # DİKKAT: %s ile parametrik sorgu yazıyoruz (SQL Injection koruması).
        query = """
            SELECT id, code, name, continent, wikipedia_link, keywords
            FROM countries
            WHERE code = %s;
        """

        # Parametreler her zaman tuple olarak verilir: (country_code,)
        cursor.execute(query, (country_code,))
        return cursor.fetchone()  # Kod benzersiz olduğu için tek satır beklenir

    except Exception as e:
        print(f"❌ Ülke bilgisi çekilirken hata oluştu: {e}")
        return None

    finally:
        # Veritabanı kaynaklarını her durumda serbest bırak
        if cursor:
            cursor.close()
        conn.close()


def insert_country(country_id, code, name, continent, wikipedia_link=None, keywords=None):
    """
    countries tablosuna yeni bir ülke ekler (Temel CRUD - INSERT).
    wikipedia_link ve keywords verilmezse NULL olarak kaydedilir.
    Başarılıysa True; aynı id/code zaten varsa, kıta kodu geçersizse
    veya başka bir hata olursa False döner.
    """
    conn = get_connection()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO countries (id, code, name, continent, wikipedia_link, keywords)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(query, (country_id, code, name, continent, wikipedia_link, keywords))

        # INSERT'in veritabanına kalıcı olarak yazılması için commit şart
        conn.commit()
        print(f"✅ {name} ({code}) başarıyla veritabanına eklendi.")
        return True

    except Exception as e:
        print(f"❌ Ülke eklenirken hata: {e}")
        # Hata durumunda yarım kalan işlemi geri al
        conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()


# Dosya doğrudan çalıştırıldığında test işlemleri yapar:
#   python -m backend.countries_manager
if __name__ == "__main__":
    print("--- 🌍 Ülke Yöneticisi Testi Başlıyor ---")

    # 1. SELECT Testi: Türkiye'yi arayalım
    print("\n[TEST 1] Ülke aranıyor: TR")
    turkey = get_country_by_code("TR")
    if turkey:
        print(f"Bulunan Kayıt: ID={turkey[0]}, Kod={turkey[1]}, İsim={turkey[2]}, Kıta={turkey[3]}")
    else:
        print("TR bulunamadı (veriler yüklenmemiş olabilir).")

    # 2. INSERT Testi: Hayali bir test ülkesi ekleyelim
    # (Test ikinci kez çalıştırılırsa bu id/code zaten var olacağı için
    #  hata verip rollback yapar; bu beklenen davranıştır.)
    print("\n[TEST 2] Yeni ülke ekleniyor: QZ")
    insert_country(
        country_id=999999,
        code="QZ",
        name="Test Ülkesi",
        continent="EU",
    )

    # 3. Negatif Test: Geçersiz kıta kodu (XX)
    # chk_countries_continent kısıtı bunu reddetmeli; fonksiyon rollback yapıp False dönmeli.
    print("\n[TEST 3] Geçersiz kıta koduyla (XX) ülke eklenmeye çalışılıyor")
    insert_country(
        country_id=999998,
        code="QY",
        name="Geçersiz Test Ülkesi",
        continent="XX",
    )
