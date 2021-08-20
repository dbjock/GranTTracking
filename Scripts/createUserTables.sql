--
-- Text encoding used: System
--
-- WARNING! All user data WILL be lost
--      This will DROP and recreate tables
PRAGMA foreign_keys = off;

-- Table: car
DROP TABLE IF EXISTS car;
CREATE TABLE car (
    id            INTEGER PRIMARY KEY,
    model         TEXT    NOT NULL
                          COLLATE NOCASE
                          UNIQUE,
    mfg_id        INTEGER REFERENCES manufacture (id) ON DELETE RESTRICT
                          NOT NULL,
    cat_id        INTEGER REFERENCES category (id) ON DELETE RESTRICT
                          NOT NULL,
    drivetrain_id INTEGER NOT NULL
                          REFERENCES drivetrain (id) ON DELETE RESTRICT
                          NOT NULL,
    year          INTEGER
);

-- Table: car_settings
DROP TABLE IF EXISTS car_settings;
CREATE TABLE car_settings (
    id              INTEGER PRIMARY KEY
                            NOT NULL,
    car_id                  REFERENCES car (id) ON DELETE RESTRICT
                                                ON UPDATE CASCADE
                            NOT NULL,
    name            TEXT    NOT NULL,
    maxpower        DECIMAL NOT NULL,
    maxtorque       DECIMAL NOT NULL,
    powerration     INTEGER NOT NULL,
    cat_id          INTEGER REFERENCES category (id) ON DELETE RESTRICT
                                                     ON UPDATE CASCADE
                            NOT NULL,
    weight          INTEGER NOT NULL,
    WeightReduction INTEGER NOT NULL,
    tire_code       TEXT    REFERENCES tire (code) ON DELETE RESTRICT
                                                   ON UPDATE CASCADE
                            NOT NULL
);

PRAGMA foreign_keys = on;