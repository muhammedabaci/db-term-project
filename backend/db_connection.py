import os
import psycopg2
from dotenv import load_dotenv

# Proje ana dizinindeki .env dosyasını bulup içindeki değişkenleri hafızaya alır
load_dotenv()

def get_connection():
    """
    PostgreSQL veritabanına bağlanır ve connection nesnesini döndürür.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="54321",           # docker-compose'daki dış port (host port)
            database="ourairports", # POSTGRES_DB değeri
            user="admin",           # POSTGRES_USER değeri
            password=os.environ.get("DB_PASSWORD") # .env'den gelen şifre
        )
        return conn
    except psycopg2.Error as e:
        print(f"❌ Veritabanı bağlantısı başarısız oldu: {e}")
        return None

# TEST
if __name__ == "__main__":
    test_conn = get_connection()
    if test_conn:
        print("✅ Veritabanına başarıyla bağlanıldı!")
        test_conn.close()