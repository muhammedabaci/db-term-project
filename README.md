# ✈️ Havacılık Veritabanı Projesi (Aviation Database)

Bu proje, İstanbul Teknik Üniversitesi (İTÜ) Veritabanı Sistemleri dersi kapsamında geliştirilen, havacılık verilerinin (havalimanları, pistler, frekanslar, navigasyon araçları vb.) ilişkisel bir veritabanı (RDBMS) üzerinde tutulmasını ve yönetilmesini sağlayan bir altyapı projesidir.

## 👥 Proje Ekibi (Grup 1)

| Öğrenci No | İsim Soyisim |
| :--- | :--- |
| 820240705 | Muhammed Abacı |
| 820230307 | Said Sezer |
| 820220712 | Muhammed Sait Alçın |
| 820230315 | Osman Nuri Akdeniz |
| 820220317 | Umut Şener |

## 📂 Proje Mimarisi ve Dizin Yapısı

```text
.
├── .github/
│   └── ISSUE_TEMPLATE/     # GitHub görev ve hata şablonları (bug.md, task.md)
├── backend/                # Python CRUD yöneticileri (db_connection.py ve *_manager.py)
├── data/                   # Veritabanına aktarılacak ham CSV dosyaları
├── sql_scripts/            # İskelet (01), kısıtlamalar (02) ve otomatik veri ekleme (03)
├── .gitignore              # Git takibi dışında bırakılan dosyalar (.env, venv/ vb.)
├── README.md               # Proje dokümantasyonu
├── docker-compose.yml      # PostgreSQL 15 Docker yapılandırması (Port: 54321:5432)
└── requirements.txt        # Python kütüphaneleri (psycopg2-binary, python-dotenv)
```

## 🚀 Kurulum ve Çalıştırma (Docker & Python)

Projeyi bilgisayarınızda ayağa kaldırmak için **Docker** ve **Python 3.9+** kurulu olmalıdır. Kök dizinde veritabanı şifrenizi barındıran bir `.env` dosyası (örneğin: `DB_PASSWORD=gizlisifre`) bulunması zorunludur.

### 1. Veritabanının Ayağa Kaldırılması
Terminali projenin ana dizininde açarak aşağıdaki komutu çalıştırın:
```bash
docker-compose up -d
```
*⚠️ Temiz Kurulum (Clean Install): Docker'ın güncel SQL dosyalarımızı otomatik okuyabilmesi için, projeyi GitHub'dan güncellediğinizde `docker-compose down -v` komutuyla eski hafızayı silip sistemi sıfırdan ayağa kaldırmalısınız.*

### 2. Python Backend (Sanal Ortam) Kurulumu
Windows terminalinde sırasıyla şu komutları çalıştırarak izole ortamı kurun ve kütüphaneleri yükleyin:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 🧪 Tablo Yöneticileri ve Testler

Takımımız, `backend` klasörü altındaki yöneticileri (manager) `%s` parametrik yapısıyla (SQL Injection koruması) kodlamış olup, tüm veri ekleme işlemlerinde `COMMIT`/`ROLLBACK` işlem güvenliği sağlanmıştır. Modülleri lokalde test etmek için modül bayrağını (`-m`) kullanabilirsiniz (örn: `python -m backend.airports_manager`).

| Veritabanı Tablosu | Python Yöneticisi | İşlemler (CRUD) | Kapsam ve Notlar |
| :--- | :--- | :--- | :--- |
| `airports` | `airports_manager.py` | SELECT, INSERT | Transaction güvenliği (`commit/rollback`) sağlandı. |
| `airport_comments` | `airport_comments_manager.py` | SELECT, INSERT | Tarih ekleme işleminde SQL `NOW()` fonksiyonu kullanıldı. |
| `airport_frequencies` | `airport_frequencies_manager.py` | SELECT, INSERT | Frekanslar tipe göre filtrelenip sıralandı. |
| `countries` | `countries_manager.py` | SELECT, INSERT | `chk_countries_continent` kısıtlaması için negatif testler yazıldı. |
| `navaids` | `navaids_manager.py` | SELECT, INSERT | Boş stringleri SQL `NULL` değerine çeviren `_empty_to_none` eklendi. |
| `regions` | `regions_manager.py` | SELECT, INSERT | `fk_regions_country` referans bütünlüğü rollback ile test edildi. |
| `runways` | `runways_manager.py` | SELECT, INSERT | Type Hinting ve spesifik `psycopg2.Error` hata yakalaması eklendi. |

## 8. Hafta: Pist Analitik Raporları

`backend/analytics_runways.py`, Said Sezer'in pist analizi görevlerini içerir:

- `get_lighted_runways(min_length_ft)`: Uzunluğu verilen feet değerinden büyük,
  aydınlatmalı pistleri havalimanı ve bölge adlarıyla getirir. Satırlar
  `(runway_id, airport_name, region_name, surface, length_ft)` biçimindedir;
  en uzun pist önce gelir.
- `get_surfaces_with_many_runways(min_runway_count=1000)`: Dünya genelindeki
  pistleri yüzey değerine göre gruplar; eşikten fazla kaydı bulunan grupları
  `(surface, total_runways)` biçiminde, sayı azalan sırada getirir.
  `ASPH` ve `ASP` gibi farklı yüzey değerleri ayrı gruplar olarak korunur.

İki fonksiyon da sonuç bulunamadığında veya bağlantı/sorgu hatasında `[]`
döndürür. Parametreler `%s` ile bağlanır ve bağlantılar `finally` içinde kapatılır.

Örnek raporları çalıştırmak için proje kökünde:

```bash
python -m backend.analytics_runways
```

Testleri çalıştırmak için:

```bash
python -m unittest discover -s tests -v
# PostgreSQL çalışırken entegrasyon testlerini de etkinleştirmek için (macOS/Linux):
RUN_DB_TESTS=1 python -m unittest discover -s tests -v
```

PowerShell'de entegrasyon testlerinden önce `$env:RUN_DB_TESTS = "1"` ayarlanır.
Entegrasyon testleri mevcut bağlantı ayarlarını kullanır; test verileri yalnızca
bağlantıya özel geçici tablolara yazılır ve gerçek proje verileri değiştirilmez.

## 🔄 Takım İş Akışı (Git Flow & Pull Requests)

Projemizin bütünlüğünü korumak ve çakışmaları (Merge Conflict) önlemek amacıyla doğrudan `main` dalına kod göndermek (Push) **yasaklanmıştır.** Ekip üyelerinin şu adımları izlemesi gerekmektedir:

1. **Güncel Kodu Alma:** Çalışmaya başlamadan önce ana kodu güncelleyin.
   ```bash
   git checkout main
   git pull
   ```
2. **Görev Dalı (Branch) Açma:** Üzerinde çalışacağınız özellik için yeni bir dal açın.
   ```bash
   git checkout -b feat/add-tablo-adi
   ```
3. **Kodlama ve Test:** Değişikliklerinizi yapın ve Docker üzerinde lokal olarak test edin.
4. **Push ve PR:** Kodlarınızı kendi dalınıza pushlayın ve GitHub üzerinden bir **Pull Request (PR)** açın.
5. **Code Review:** Açılan PR, en az 1 yetkili (Reviewer) tarafından onaylandıktan (Approve) sonra `main` dalına birleştirilecektir (Merge).

## 📅 Proje Yol Haritası (Roadmap)

Projemizin 5. ile 10. haftalar arasındaki çevik (agile) geliştirme süreci aşağıdaki takvime göre yürütülmektedir:

- [x] **Hafta 5: Veritabanı İskeleti ve Veri Aktarımı** (`CREATE TABLE`).
- [x] **Hafta 6: İlişkisel Mimari ve Kısıtlamalar** (`ALTER TABLE`, Foreign Keys, UNIQUE).
- [x] **Hafta 7: Backend Entegrasyonu ve Temel CRUD** (Python `psycopg2`, Manager dosyaları).
- [ ] **Hafta 8: Kompleks SQL Sorguları ve Analitik** (`JOIN`, `GROUP BY`).
- [ ] **Hafta 9: CLI Arayüzü, Hata Yönetimi ve Güvenlik.**
- [ ] **Hafta 10: Optimizasyon, Dokümantasyon ve Teslim.**
