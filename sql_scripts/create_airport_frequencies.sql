CREATE TABLE airport_frequencies (
    id              INTEGER PRIMARY KEY,
    airport_ref     INTEGER NOT NULL,
    airport_ident   VARCHAR(20),
    type            VARCHAR(30),
    description     TEXT,
    frequency_mhz   NUMERIC(7,3)
);
