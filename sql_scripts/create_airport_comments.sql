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
