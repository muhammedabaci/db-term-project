-- 1. Navaids tablosunun bağlanabilmesi için ident sütununu benzersiz (UNIQUE) yapıyoruz
ALTER TABLE airports 
ADD CONSTRAINT uq_airports_ident UNIQUE (ident);

-- 2. Ülkeler tablosuna bağlantı (Foreign Key)
ALTER TABLE airports 
ADD CONSTRAINT fk_airports_country 
FOREIGN KEY (iso_country) REFERENCES countries(code);

-- 3. Bölgeler tablosuna bağlantı (Foreign Key)
ALTER TABLE airports 
ADD CONSTRAINT fk_airports_region 
FOREIGN KEY (iso_region) REFERENCES regions(code);