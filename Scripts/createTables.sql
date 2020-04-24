--
-- 4/15/2020
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
-- Table: car
CREATE TABLE car (
    id            INTEGER      PRIMARY KEY,
    model         VARCHAR (16) NOT NULL
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
CREATE TABLE category (
    id          INTEGER      PRIMARY KEY,
    name        VARCHAR (16) UNIQUE
                             NOT NULL
							 COLLATE NOCASE,
    description TEXT
);

-- Table: circuit
CREATE TABLE circuit (
    id   INTEGER      PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (16) UNIQUE
	                  COLLATE NOCASE
);

-- Table: country
CREATE TABLE country (
    ID     INTEGER      PRIMARY KEY AUTOINCREMENT,
    name   VARCHAR (64) COLLATE NOCASE,
    alpha2 CHAR (2)     UNIQUE
                        NOT NULL,
    alpha3 CHAR (3)     NOT NULL
                        UNIQUE,
    region VARCHAR (32) 
);

-- Table: drivetrain
CREATE TABLE drivetrain (
    id          INTEGER PRIMARY KEY,
    code        TEXT    UNIQUE
                        NOT NULL
                        CHECK (length(code) <= 5),
    description TEXT
);

-- Table: league
CREATE TABLE league (
    id      INTEGER      PRIMARY KEY AUTOINCREMENT,
    name    VARCHAR (16) UNIQUE
                         NOT NULL
                         COLLATE NOCASE,
    sortord INTEGER      UNIQUE
);

-- Table: manufacture
CREATE TABLE manufacture (
    id         INTEGER      PRIMARY KEY,
    name       VARCHAR (32) UNIQUE
                            NOT NULL
                            COLLATE NOCASE,
    country_id INTEGER      REFERENCES country (ID) 
                            NOT NULL
);
-- Table: race
CREATE TABLE race (ID INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (18) COLLATE NOCASE, tl_id INTEGER REFERENCES track_layout (id) ON DELETE RESTRICT NOT NULL, time TIME, weather_id INTEGER REFERENCES weather (id) ON DELETE RESTRICT, laps INTEGER, type_id INTEGER REFERENCES race_type (ID) ON DELETE RESTRICT NOT NULL, time_limit TIME, cat_id INTEGER REFERENCES category (id) ON DELETE RESTRICT, cars INTEGER, start_grid INTEGER, prize1 INTEGER, prize2 INTEGER, prize3 INTEGER, notes TEXT);

-- Table: race_collection
CREATE TABLE race_collection (id INTEGER PRIMARY KEY AUTOINCREMENT, league_id INTEGER REFERENCES league (id) ON DELETE RESTRICT NOT NULL, name VARCHAR (16));

-- Table: race_type
CREATE TABLE race_type (
    ID   INTEGER      PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (16) UNIQUE
                      NOT NULL
                      COLLATE NOCASE
);

-- Table: track
CREATE TABLE track (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR (40) UNIQUE
                            NOT NULL
							COLLATE NOCASE,
    country_id INTEGER      REFERENCES country (ID) ON DELETE RESTRICT
);

-- Table: track_layout
CREATE TABLE track_layout (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,
    track_id   INTEGER      REFERENCES track (id) ON DELETE RESTRICT
                            NOT NULL,
    name       VARCHAR (16) COLLATE NOCASE,
    miles      DECIMAL      NOT NULL,
    circuit_id INTEGER      REFERENCES circuit (id) ON DELETE RESTRICT
                            NOT NULL
);

-- Table: weather
CREATE TABLE weather (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (16) UNIQUE NOT NULL);

-- Index: sortord
CREATE INDEX sortord ON league (sortord COLLATE RTRIM ASC);

PRAGMA foreign_keys = on;
