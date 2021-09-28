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
DROP TABLE IF EXISTS car_setting;
CREATE TABLE car_setting (
    id               INTEGER PRIMARY KEY
                             NOT NULL,
    car_id           INTEGER REFERENCES car (id) ON DELETE CASCADE
                                                 ON UPDATE CASCADE
                             NOT NULL,
    cat_id           INTEGER REFERENCES category (id) ON DELETE RESTRICT
                                                      ON UPDATE CASCADE
                             NOT NULL,
    name             TEXT    NOT NULL,
    max_power        INTEGER,
    max_torque       REAL,
    power_ratio      INTEGER,
    traction_control INTEGER,
    brake_balance    INTEGER,
    top_speed        INTEGER,
    gear_1           TEXT,
    gear_2           TEXT,
    gear_3           TEXT,
    gear_4           TEXT,
    gear_5           TEXT,
    gear_6           TEXT,
    gear_7           TEXT,
    final_gear       TEXT,
    weight           INTEGER,
    weight_reduction INTEGER,
    tire_code        TEXT    REFERENCES tire (code) ON DELETE RESTRICT
                                                    ON UPDATE CASCADE,
    accel            REAL,
    braking          REAL,
    cornering        REAL,
    max_speed        REAL,
    stability        REAL
);



PRAGMA foreign_keys = on;