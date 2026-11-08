-- Navaids refer to the airport identifier and country code.
-- This migration depends on 02_alter_airports.sql, which makes airports.ident unique.
ALTER TABLE navaids
    ADD CONSTRAINT fk_navaids_airport
    FOREIGN KEY (associated_airport) REFERENCES airports(ident);

ALTER TABLE navaids
    ADD CONSTRAINT fk_navaids_country
    FOREIGN KEY (iso_country) REFERENCES countries(code);
