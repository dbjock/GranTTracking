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

PRAGMA foreign_keys = on;