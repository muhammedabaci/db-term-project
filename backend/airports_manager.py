# backend/airports_manager.py

from backend.db_connection import get_connection

def get_airport_by_ident(ident_code):
    """
    Belirtilen ICAO/IATA koduna (ident) sahip havalimanının temel bilgilerini getirir.
    """
    conn = get_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        
        # DİKKAT: %s kullanarak SQL Injection'a karşı parametrik sorgu yazıyoruz.
        query = """
            SELECT id, ident, name, type, iso_country 
            FROM airports 
            WHERE ident = %s;
        """
        
        # Parametreler her zaman tuple (demet) olarak verilmelidir: (ident_code,)
        cursor.execute(query, (ident_code,))
        record = cursor.fetchone() # Sadece tek bir satır beklediğimiz için fetchone()
        
        return record
        
    except Exception as e:
        print(f"❌ Havalimanı bilgisi çekilirken hata oluştu: {e}")
        return None
        
    finally:
        # Hafıza sızıntısını ve veritabanı kilitlenmelerini önlemek için temizlik
        if 'cursor' in locals() and cursor: cursor.close()
        if 'conn' in locals() and conn: conn.close()

def insert_basic_airport(airport_id, ident, name, airport_type, iso_country):
    """
    Sisteme yeni bir havalimanı ekler (Temel CRUD - INSERT operasyonu).
    """
    conn = get_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO airports (id, ident, name, type, iso_country) 
            VALUES (%s, %s, %s, %s, %s);
        """
        
        cursor.execute(query, (airport_id, ident, name, airport_type, iso_country))
        
        # INSERT işlemlerinde değişikliği fiziksel olarak diske yazmak için commit ŞARTTIR
        conn.commit() 
        print(f"✅ {name} ({ident}) başarıyla veritabanına eklendi.")
        return True
        
    except Exception as e:
        print(f"❌ Havalimanı eklenirken hata: {e}")
        # Bir hata olursa (örneğin aynı ID'den varsa), veritabanı çökmesin diye işlemi geri al
        conn.rollback() 
        return False
        
    finally:
        if 'cursor' in locals() and cursor: cursor.close()
        if 'conn' in locals() and conn: conn.close()

# Dosya doğrudan terminalden çalıştırıldığında test işlemleri yapar
if __name__ == "__main__":
    print("--- ✈️ Havalimanı Yöneticisi Testi Başlıyor ---")
    
    # 1. SELECT Testi: İstanbul Havalimanı'nı (LTFM) arayalım
    print("\n[TEST 1] Havalimanı Aranıyor: LTFM")
    ltfm = get_airport_by_ident('LTFM')
    if ltfm:
        print(f"Bulunan Kayıt: ID={ltfm[0]}, Kod={ltfm[1]}, İsim={ltfm[2]}, Ülke={ltfm[4]}")
    else:
        print("LTFM bulunamadı (Veriler tam yüklenmemiş olabilir).")

    # 2. INSERT Testi: Sisteme hayali bir test havalimanı ekleyelim
    # (Eğer bu ID veya ident zaten varsa except bloğuna düşüp rollback yapacaktır)
    print("\n[TEST 2] Yeni Havalimanı Ekleniyor...")
    insert_result = insert_basic_airport(
        airport_id=999999, 
        ident="TEST-01", 
        name="İTÜ KKTC Test Havalimanı", 
        airport_type="small_airport", 
        iso_country="TR"
    )