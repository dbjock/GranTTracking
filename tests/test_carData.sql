--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;

INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (1, 'Test Car A', 5, 5, 3, 2012);
INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (2, 'Test Car B', 3, 3, 5, 2015);
INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (3, 'Test Car AA', 11, 9, 5, 2021);
INSERT INTO car (id, model, mfg_id, cat_id, drivetrain_id, year) VALUES (4, 'Check Me out', 3, 9, 3, 2021);

-- Table: car_setting
-- This requires the car table be populated first
INSERT INTO car_setting (id, car_id, cat_id, name) VALUES (1, 1, 14, 'IB3F0SK1');
INSERT INTO car_setting (id, car_id, cat_id, name, max_power, max_torque, power_ratio, traction_control, brake_balance, top_speed, gear_1, gear_2, gear_3, gear_4, gear_5, gear_6, gear_7, final_gear, weight, weight_reduction, tire_code, accel, braking, cornering, max_speed, stability) VALUES (2, 1, 11, 'H18TEAX3ZPMZ8GRMUA', 34, 10.0, 23, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 22, 27, 'SH', NULL, NULL, NULL, NULL, NULL);
INSERT INTO car_setting (id, car_id, cat_id, name, max_power, max_torque, power_ratio, traction_control, brake_balance, top_speed, gear_1, gear_2, gear_3, gear_4, gear_5, gear_6, gear_7, final_gear, weight, weight_reduction, tire_code, accel, braking, cornering, max_speed, stability) VALUES (3, 2, 2, '37C92PRQA8WX2FP', 26, 987.3, 12, 2, -4, 400, '1.2345/10', '1.0345/20', '1.0045/30', '1.0005/40', '0.1005/50', '0.1605/60', '0.1707/70', '3.1600', 1500, 24, 'RHW', 9.9, 8.0, 7.2, 6.0, 2.3);
INSERT INTO car_setting (id, car_id, cat_id, name, max_power, max_torque, power_ratio, traction_control, brake_balance, top_speed, gear_1, gear_2, gear_3, gear_4, gear_5, gear_6, gear_7, final_gear, weight, weight_reduction, tire_code, accel, braking, cornering, max_speed, stability) VALUES (4, 3, 2, 'W0Q20BW19N9O49DKJYN', 26, 987.3, 18, 2, -8, 480, '1.2345/10', '1.0345/20', '1.0045/30', '1.0005/40', '0.1005/50', '0.1605/60', '0.1707/70', '3.1600', 10500, 24, 'RHW', 9.9, 8.0, 7.2, 6.0, 2.3);
INSERT INTO car_setting (id, car_id, cat_id, name, max_power, max_torque, power_ratio, traction_control, brake_balance, top_speed, gear_1, gear_2, gear_3, gear_4, gear_5, gear_6, gear_7, final_gear, weight, weight_reduction, tire_code, accel, braking, cornering, max_speed, stability) VALUES (5, 3, 1, 'CCB9', 56, 73.0, 58, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 47, 67, 'RSS', NULL, NULL, NULL, NULL, NULL);

PRAGMA foreign_keys = on;
