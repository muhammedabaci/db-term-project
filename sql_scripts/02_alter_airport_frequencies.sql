ALTER TABLE airport_frequencies
    ADD CONSTRAINT fk_airport_frequencies_airport
    FOREIGN KEY (airport_ref) REFERENCES airports(id);
