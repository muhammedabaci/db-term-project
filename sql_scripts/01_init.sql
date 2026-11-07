-- =======================================================
-- AVIATION DBMS - DATABASE INITIALIZATION SCRIPT
-- =======================================================

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

CREATE TABLE airports (
    id INT PRIMARY KEY,
    ident VARCHAR(20),
    type VARCHAR(50),
    name VARCHAR(255),
    latitude_deg DECIMAL,
    longitude_deg DECIMAL,
    elevation_ft INT,
    continent VARCHAR(10),
    iso_country VARCHAR(10),
    iso_region VARCHAR(20),
    municipality VARCHAR(255),
    scheduled_service VARCHAR(10),
    icao_code VARCHAR(20),
    iata_code VARCHAR(20),
    gps_code VARCHAR(20),
    local_code VARCHAR(20),
    home_link TEXT,
    wikipedia_link TEXT,
    keywords TEXT
);

CREATE TABLE runways (
    id INT PRIMARY KEY,
    airport_ref INT,
    airport_ident VARCHAR(20),
    length_ft INT,
    width_ft INT,
    surface VARCHAR(100),
    lighted INT,
    closed INT,
    le_ident VARCHAR(20),
    le_latitude_deg DECIMAL,
    le_longitude_deg DECIMAL,
    le_elevation_ft INT,
    le_heading_degT DECIMAL,
    le_displaced_threshold_ft INT,
    he_ident VARCHAR(20),
    he_latitude_deg DECIMAL,
    he_longitude_deg DECIMAL,
    he_elevation_ft INT,
    he_heading_degT DECIMAL,
    he_displaced_threshold_ft INT
);

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

CREATE TABLE navaids (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    ident VARCHAR(20),
    name VARCHAR(100),
    type VARCHAR(50),
    frequency_khz INTEGER,
    latitude_deg DOUBLE PRECISION,
    longitude_deg DOUBLE PRECISION,
    elevation_ft INTEGER,
    iso_country VARCHAR(10),
    dme_frequency_khz INTEGER,
    dme_channel TEXT,
    dme_latitude_deg DOUBLE PRECISION,
    dme_longitude_deg DOUBLE PRECISION,
    dme_elevation_ft INTEGER,
    slaved_variation_deg DOUBLE PRECISION,
    magnetic_variation_deg DOUBLE PRECISION,
    usageType TEXT,
    power VARCHAR(20),
    associated_airport VARCHAR(20)
);