-- runways tablosu için
ALTER TABLE runways
ADD CONSTRAINT fk_runways_airport
FOREIGN KEY (airport_ref) REFERENCES airports(id);

-- airport_frequencies tablosu için
ALTER TABLE airport_frequencies
ADD CONSTRAINT fk_frequencies_airport
FOREIGN KEY (airport_ref) REFERENCES airports(id);

-- airport_comments tablosu için
ALTER TABLE airport_comments
ADD CONSTRAINT fk_comments_airport
FOREIGN KEY (airport_ref) REFERENCES airports(id);

