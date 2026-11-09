-- 1. En bağımsız tablo: Ülkeler
COPY countries FROM '/csv_data/countries.csv' DELIMITER ',' CSV HEADER;

-- 2. Ülkelere bağlı: Bölgeler
COPY regions FROM '/csv_data/regions.csv' DELIMITER ',' CSV HEADER;

-- 3. Ülke ve Bölgelere bağlı: Havalimanları
COPY airports FROM '/csv_data/airports.csv' DELIMITER ',' CSV HEADER;

-- 4. Havalimanlarına bağlı olan alt tablolar (Sırası kendi içinde fark etmez)
COPY runways FROM '/csv_data/runways.csv' DELIMITER ',' CSV HEADER;
COPY airport_frequencies FROM '/csv_data/airport_frequencies.csv' DELIMITER ',' CSV HEADER;
COPY airport_comments FROM '/csv_data/airport_comments.csv' DELIMITER ',' CSV HEADER;
COPY navaids FROM '/csv_data/navaids.csv' DELIMITER ',' CSV HEADER;