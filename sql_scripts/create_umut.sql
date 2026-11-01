CREATE TABLE airport_frequencies (
    id              INTEGER PRIMARY KEY,
    airport_ref     INTEGER NOT NULL,
    airport_ident   VARCHAR(20),
    type            VARCHAR(30),
    description     TEXT,
    frequency_mhz   NUMERIC(7,3)
);

CREATE TABLE airport_comments (
    id               INTEGER PRIMARY KEY,
    thread_ref       INTEGER,
    airport_ref      INTEGER NOT NULL,
    airport_ident    VARCHAR(20),
    comment_date     TIMESTAMP,
    member_nickname  VARCHAR(100),
    subject          TEXT,
    body             TEXT
);
