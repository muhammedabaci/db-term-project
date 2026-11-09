# ✈️ Havacılık Veritabanı Projesi (Aviation Database)

Bu proje, İstanbul Teknik Üniversitesi (İTÜ) Veritabanı Sistemleri dersi kapsamında geliştirilen, havacılık verilerinin (havalimanları, pistler, frekanslar, navigasyon araçları vb.) ilişkisel bir veritabanı (RDBMS) üzerinde tutulmasını ve yönetilmesini sağlayan bir altyapı projesidir.

## 👥 Proje Ekibi (Grup 1)

* **Muhammed ABACI** - 820240705
* **Said SEZER** - 820230307
* **Muhammed Sait ALÇIN** - 820220712
* **Osman Nuri AKDENİZ** - 820230315
* **Umut ŞENER** - 820220317

## 📅 Proje Yol Haritası (Roadmap)

Projemizin 5. ile 10. haftalar arasındaki çevik (agile) geliştirme süreci aşağıdaki takvime göre planlanmış ve yürütülmektedir:

- [x] **Hafta 5: Veritabanı İskeleti ve Veri Aktarımı**
  - Tüm ilişkisel tabloların `CREATE TABLE` ile fiziksel olarak oluşturulması ve lokal testleri.
- [x] **Hafta 6: İlişkisel Mimari ve Kısıtlamalar (Foreign Keys)**
  - Bağımsız tabloların `ALTER TABLE` ile `Primary Key`, `Foreign Key` ve `UNIQUE` kısıtlamaları kullanılarak birbirine bağlanması ve Docker entegrasyonu.
- [ ] **Hafta 7: Backend Entegrasyonu ve Temel CRUD Operasyonları**
  - Python `psycopg2` ile ana veritabanı bağlantısının kurulması, temel `SELECT` ve `INSERT` fonksiyonlarının modüler olarak yazılması.
- [ ] **Hafta 8: Kompleks SQL Sorguları ve Analitik**
  - Birden fazla tablonun birleştiği (`JOIN`), gruplandığı (`GROUP BY`) ve filtrelendiği iş kurallarına uygun gerçek dünya sorgularının geliştirilmesi.
- [ ] **Hafta 9: CLI Arayüzü, Hata Yönetimi ve Güvenlik**
  - Projenin terminal (CLI) menüsüne bağlanması, hata durumları için `try-except` blokları ve `Transaction` (`COMMIT`/`ROLLBACK`) mantığının kurulması.
- [ ] **Hafta 10: Optimizasyon, Dokümantasyon ve Teslim**
  - ER diyagramının çıkarılması, kod optimizasyonu ve projenin GitHub üzerinde eksiksiz belgelenmesi.

## 🏗️ Proje Mimarisi ve Klasör Yapısı

Projemiz, Docker üzerinde çalışan bir **PostgreSQL 15** veritabanı üzerine inşa edilmiştir. Veritabanı şemamız (Schema) modüler bir yapıda tasarlanmış olup, kurulum komutları alfabetik sırayla çalışması için `sql_scripts/` klasörü altında numaralandırılmıştır:

* `01_init.sql`: Tüm çıplak tabloların (`CREATE TABLE`) oluşturulduğu temel iskelet dosyası.
* `02_alter_[tablo_adi].sql`: Tablolar arası ilişkilerin (Foreign Keys) ve kısıtlamaların (Unique vb.) tanımlandığı, veri bütünlüğünü sağlayan köprü dosyaları.
* `03_insert_data.sql`: *(Yakında eklenecek)* Ham verilerin (CSV) tablolara otomatik aktarılmasını sağlayan dosya.

## 🚀 Kurulum ve Çalıştırma (Docker Otomasyonu)

Projeyi kendi bilgisayarınızda ayağa kaldırmak için **Docker** ve **Docker Compose** kurulu olmalıdır.

Terminali projenin ana dizininde açarak aşağıdaki komutu çalıştırın:
```bash
docker-compose up -d
```
Bu komut, PostgreSQL motorunu başlatır ve `sql_scripts` klasöründeki dosyaları okuyarak tüm veritabanı mimarisini otomatik olarak kurar.

### ⚠️ Kritik Uyarı: Temiz Kurulum (Clean Install)
Docker'ın güncel SQL dosyalarımızı (01, 02 vb.) otomatik okuyabilmesi için, kurulumun "Sıfır Kilometre" yapılması şarttır. Projeyi GitHub'dan güncellediğinizde (`git pull`), sistemi ayağa kaldırmadan önce **mutlaka eski veritabanı hafızasını (volume) silmelisiniz:**

```bash
# 1. Eski sistemi ve veritabanı kalıntılarını tamamen siler
docker-compose down -v

# 2. Güncel kodlarla sistemi sıfırdan kurar
docker-compose up -d
```

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