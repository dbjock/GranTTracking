--
-- 05/28/2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
-- Table: car
DROP TABLE IF EXISTS car;
CREATE TABLE car (
    id            INTEGER      PRIMARY KEY,
    model         TEXT NOT NULL
							   COLLATE NOCASE,
    mfg_id        INTEGER      REFERENCES manufacture (id) ON DELETE RESTRICT
                               NOT NULL,
    cat_id        INTEGER      REFERENCES category (id) ON DELETE RESTRICT
                               NOT NULL,
    drivetrain_id INTEGER      NOT NULL
                               REFERENCES drivetrain (id) ON DELETE RESTRICT
                               NOT NULL,
    year          INTEGER,
    displacement  TEXT,
    length_in     DECIMAL,
    width_in      DECIMAL,
    height_in     DECIMAL,
    weight_lb     DECIMAL,
    max_power     INTEGER,
    max_torque    INTEGER
);

-- Table: category
DROP TABLE IF EXISTS category;
CREATE TABLE category (
    id          INTEGER      PRIMARY KEY,
    name        TEXT UNIQUE
                             NOT NULL
                             COLLATE NOCASE,
    description TEXT,
    sortOrder   INTEGER
);

-- Table: circuit
DROP TABLE IF EXISTS circuit;
CREATE TABLE circuit (
    id   INTEGER      PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
	                  COLLATE NOCASE
);

-- Table: country
DROP TABLE IF EXISTS country;
CREATE TABLE country (
    ID     INTEGER      PRIMARY KEY AUTOINCREMENT,
    name   TEXT COLLATE NOCASE,
    alpha2 CHAR (2)     UNIQUE
                        NOT NULL,
    alpha3 CHAR (3)     NOT NULL
                        UNIQUE,
    region TEXT
);

-- Table: drivetrain
DROP TABLE IF EXISTS drivetrain;
CREATE TABLE drivetrain (
    id          INTEGER PRIMARY KEY,
    code        TEXT    UNIQUE
                        NOT NULL
                        CHECK (length(code) <= 5),
    description TEXT
);

-- Table: league
DROP TABLE IF EXISTS league;
CREATE TABLE league (
    id      INTEGER      PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE
                         NOT NULL
                         COLLATE NOCASE,
    sortord INTEGER      UNIQUE
);

-- Table: manufacture
DROP TABLE IF EXISTS manufacture;
CREATE TABLE manufacture (
    id         INTEGER      PRIMARY KEY,
    name       TEXT UNIQUE
                            NOT NULL
                            COLLATE NOCASE,
    country_id INTEGER      REFERENCES country (ID) ON DELETE RESTRICT
                            NOT NULL
);

-- Table: race
DROP TABLE IF EXISTS race;
CREATE TABLE race (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    COLLATE NOCASE
                       NOT NULL,
    tl_id      INTEGER REFERENCES track_layout (id) ON DELETE RESTRICT
                       NOT NULL,
    rc_id      INTEGER NOT NULL
                       REFERENCES race_collection (id) ON DELETE RESTRICT,
    racetime   TIME,
    weather_id INTEGER REFERENCES weather (id) ON DELETE RESTRICT,
    limits     TEXT,
    type_id    INTEGER REFERENCES race_type (ID) ON DELETE RESTRICT
                       NOT NULL,
    prize1     INTEGER,
    prize2     INTEGER,
    prize3     INTEGER,
    notes      TEXT
);

-- Table: race_collection
DROP TABLE IF EXISTS race_collection;
CREATE TABLE race_collection (
    id        INTEGER      PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER      REFERENCES league (id) ON DELETE RESTRICT
                           NOT NULL,
    name      TEXT,
    description TEXT
);

-- Table: race_type
DROP TABLE IF EXISTS race_type;
CREATE TABLE race_type (
    ID   INTEGER      PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
                      NOT NULL
                      COLLATE NOCASE
);

-- Table: track
DROP TABLE IF EXISTS track;
CREATE TABLE track (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,
    name       TEXT UNIQUE
                            NOT NULL
							COLLATE NOCASE,
    country_id INTEGER      REFERENCES country (ID) ON DELETE RESTRICT
);

-- Table: track_layout
DROP TABLE IF EXISTS track_layout;
CREATE TABLE track_layout (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,
    track_id   INTEGER      REFERENCES track (id) ON DELETE RESTRICT
                            NOT NULL,
    name       TEXT COLLATE NOCASE
                            NOT NULL,
    miles      DECIMAL      NOT NULL,
    circuit_id INTEGER      REFERENCES circuit (id) ON DELETE RESTRICT
                            NOT NULL
);

-- Table: weather
DROP TABLE IF EXISTS weather;
CREATE TABLE weather (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);

-- Index: sortord
DROP INDEX IF EXISTS sortord;
CREATE INDEX sortord ON league (sortord COLLATE RTRIM ASC);

PRAGMA foreign_keys = on;
