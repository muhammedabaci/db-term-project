CREATE TABLE countries (
    id INTEGER PRIMARY KEY,
    code VARCHAR(2) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    continent VARCHAR(2) NOT NULL,
    wikipedia_link TEXT,
    keywords TEXT,

    CONSTRAINT chk_countries_continent
        CHECK (continent IN ('AF', 'AN', 'AS', 'EU', 'NA', 'OC', 'SA'))
);