-- runways tablosu için
ALTER TABLE runways
ADD CONSTRAINT fk_runways_airport
FOREIGN KEY (airport_ref) REFERENCES airports(id);
