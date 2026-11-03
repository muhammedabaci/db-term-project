CREATE TABLE regions (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    local_code TEXT NOT NULL,
    name VARCHAR(100) NOT NULL,
    continent VARCHAR(2) NOT NULL,
    iso_country VARCHAR(2) NOT NULL,
    wikipedia_link TEXT,
    keywords TEXT,

    CONSTRAINT chk_regions_continent
        CHECK (continent IN ('AF', 'AN', 'AS', 'EU', 'NA', 'OC', 'SA'))
);