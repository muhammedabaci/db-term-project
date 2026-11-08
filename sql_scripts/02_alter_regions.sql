-- Bölgeleri ülkelere bağlama (Foreign Key)
-- Her bölgenin iso_country değeri, countries tablosunda var olan bir ülke kodu olmalı.
ALTER TABLE regions
ADD CONSTRAINT fk_regions_country
FOREIGN KEY (iso_country) REFERENCES countries(code);
