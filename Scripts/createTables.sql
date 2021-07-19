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
    notes      TEXT
);

-- Table: race_collection
DROP TABLE IF EXISTS race_collection;
CREATE TABLE race_collection (
    id        INTEGER      PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER      REFERENCES league (id) ON DELETE RESTRICT
                           NOT NULL,
    name      TEXT,
    description TEXT,
    cat_id        INTEGER      REFERENCES category (id) ON DELETE RESTRICT,
    prize1     INTEGER NOT NULL,
    prize2     INTEGER NOT NULL,
    prize3     INTEGER NOT NULL
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

-- View: vRaceCollection
DROP VIEW IF EXISTS vRaceCollection;
CREATE VIEW vRaceCollection AS
    SELECT rc.id AS collectionId,
           rc.name AS collection,
           rc.description,
           l.id AS leagueId,
           l.name AS league,
           l.sortord AS leagueSortord
      FROM race_collection AS rc
           LEFT JOIN
           league AS l ON rc.league_id = l.id;

-- View: vTrackLayout
DROP VIEW IF EXISTS vTrackLayout;
CREATE VIEW vTrackLayout AS
    SELECT t.id AS trackId,
           t.name AS track,
           l.id AS layoutId,
           l.name AS layout,
           l.miles AS Miles,
           c.id AS circuitId,
           c.name AS Circuit,
           cntry.ID AS cntryId,
           cntry.name AS Country,
           cntry.alpha2,
           cntry.alpha3,
           cntry.region AS Region
      FROM track AS t
           INNER JOIN
           track_layout AS l ON t.id = l.track_id
           LEFT JOIN
           country AS cntry ON t.country_id = cntry.ID
           INNER JOIN
           circuit AS c ON l.circuit_id = c.id;

PRAGMA foreign_keys = on;
