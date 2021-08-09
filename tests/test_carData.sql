--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;

INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (1, 'Test Car A', 5, 5, 3, 2012);
INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (2, 'Test Car B', 10, 3, 5, 2015);
INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (3, 'Test Car AA', 10, 9, 3, 2021);

PRAGMA foreign_keys = on;
