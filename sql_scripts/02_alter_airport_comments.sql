ALTER TABLE airport_comments
    ADD CONSTRAINT fk_airport_comments_airport
    FOREIGN KEY (airport_ref) REFERENCES airports(id);
