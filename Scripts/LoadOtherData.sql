--
-- 5/29/2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;

-- Table: manufacture
INSERT INTO manufacture (id, name, country_id) VALUES (1, 'Jaguar', 235);
INSERT INTO manufacture (id, name, country_id) VALUES (2, 'Aston Martin', 235);
INSERT INTO manufacture (id, name, country_id) VALUES (3, 'McLaren', 235);
INSERT INTO manufacture (id, name, country_id) VALUES (4, 'Lewis Hamilton', 235);
INSERT INTO manufacture (id, name, country_id) VALUES (5, 'Volkswagon', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (6, 'Mercedes-Benz', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (7, 'BMW', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (8, 'Audi', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (9, 'Mini', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (10, 'Porsche', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (11, 'Renault Sport', 77);
INSERT INTO manufacture (id, name, country_id) VALUES (12, 'Peugeot', 77);
INSERT INTO manufacture (id, name, country_id) VALUES (13, 'Citrogen', 77);
INSERT INTO manufacture (id, name, country_id) VALUES (14, 'Alpine', 77);
INSERT INTO manufacture (id, name, country_id) VALUES (15, 'Bugatti', 77);
INSERT INTO manufacture (id, name, country_id) VALUES (16, 'Alfa Romeo', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (17, 'Ferrari', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (18, 'Lamborghini', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (19, 'Zagato', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (20, 'De Tomaso', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (21, 'Fiat', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (22, 'Abarth', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (23, 'Lancia', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (24, 'KTM', 15);
INSERT INTO manufacture (id, name, country_id) VALUES (25, 'Super Formula', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (26, 'Toyota', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (27, 'Nissan', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (28, 'Honda', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (29, 'Mazda', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (30, 'Subaru', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (31, 'Mitsubishi Motors', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (32, 'Daihatsu', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (33, 'Lexus', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (34, 'Gran Turismo', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (35, 'Suzuki', 113);
INSERT INTO manufacture (id, name, country_id) VALUES (36, 'Hyundai', 120);
INSERT INTO manufacture (id, name, country_id) VALUES (37, 'Chevrolet', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (38, 'Ford', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (39, 'Dodge', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (40, 'Infiniti', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (41, 'Chaparral', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (42, 'Fittipaldi Motors', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (43, 'Shelby', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (44, 'Plymouth', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (45, 'Telsa', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (46, 'Pontiac', 237);
INSERT INTO manufacture (id, name, country_id) VALUES (47, 'TVR', 235);
INSERT INTO manufacture (id, name, country_id) VALUES (48, 'RUF', 84);
INSERT INTO manufacture (id, name, country_id) VALUES (49, 'Maserati', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (50, 'Renault', 77);
INSERT INTO manufacture (id, name, country_id) VALUES (51, 'Pagani', 111);
INSERT INTO manufacture (id, name, country_id) VALUES (52, 'RE Amemiya', 113);

-- Table: track
INSERT INTO track (id, name, country_id) VALUES (1, 'Northern Isle Speedway', NULL);
INSERT INTO track (id, name, country_id) VALUES (2, 'Dragon Tail', 56);
INSERT INTO track (id, name, country_id) VALUES (3, 'Colorado Springs', 237);
INSERT INTO track (id, name, country_id) VALUES (4, 'Autodrome Lago Maggiore', 111);
INSERT INTO track (id, name, country_id) VALUES (5, 'Kyoto Driving Park', 113);
INSERT INTO track (id, name, country_id) VALUES (6, 'Sardegna', 111);
INSERT INTO track (id, name, country_id) VALUES (7, 'Blue Moon Bay Speedway', 237);
INSERT INTO track (id, name, country_id) VALUES (8, 'Tsukuba Circuit', 113);
INSERT INTO track (id, name, country_id) VALUES (9, 'Brands Hatch', 235);
INSERT INTO track (id, name, country_id) VALUES (10, 'Tokyo Expressway', 113);
INSERT INTO track (id, name, country_id) VALUES (11, 'Willow Springs', 237);
INSERT INTO track (id, name, country_id) VALUES (12, 'BB Raceway', 113);
INSERT INTO track (id, name, country_id) VALUES (13, 'Suzuka Circuit', 113);
INSERT INTO track (id, name, country_id) VALUES (14, 'Autopolis International Racing Course', 113);
INSERT INTO track (id, name, country_id) VALUES (15, 'Circuit de Barcelona-Catalunya', 210);
INSERT INTO track (id, name, country_id) VALUES (16, 'Circuit de Sainte-Croix', 77);
INSERT INTO track (id, name, country_id) VALUES (17, 'Alsace - Village', 77);
INSERT INTO track (id, name, country_id) VALUES (18, 'Autoromo Nazionale Monza', 111);
INSERT INTO track (id, name, country_id) VALUES (19, 'Goodwood Motor Circuit', 235);
INSERT INTO track (id, name, country_id) VALUES (20, 'Mount Panorama Motor Racing Circuit', 14);
INSERT INTO track (id, name, country_id) VALUES (21, 'Red Bull Ring', 15);
INSERT INTO track (id, name, country_id) VALUES (22, 'Special Stage Route X', 237);
INSERT INTO track (id, name, country_id) VALUES (23, 'Fishermans Ranch', 237);
INSERT INTO track (id, name, country_id) VALUES (24, 'Circuit de Spa-Francochamps', 22);
INSERT INTO track (id, name, country_id) VALUES (25, 'Circuit de la Sarthe', 77);
INSERT INTO track (id, name, country_id) VALUES (26, 'Autodromo de Interlagos', 32);
INSERT INTO track (id, name, country_id) VALUES (27, 'Fuji International Speedway', 113);
INSERT INTO track (id, name, country_id) VALUES (28, 'Nurburgring', 84);

-- Table: track_layout
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (1, 1, 'Default', 0.56, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (2, 2, 'Seaside', 3.24, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (3, 2, 'Seaside II', 3.24, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (4, 2, 'Gardens', 2.7, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (5, 2, 'Gardens II', 2.7, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (6, 3, 'Lake', 1.86, 2);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (7, 3, 'Lake II', 1.86, 2);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (8, 4, 'GP', 3.61, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (9, 4, 'GP II', 3.61, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (10, 4, 'Center', 1.06, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (11, 4, 'East', 2.26, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (12, 4, 'West', 2.59, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (13, 4, 'Center II', 1.06, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (14, 4, 'East II', 2.26, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (15, 4, 'West II', 2.59, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (16, 5, 'Yamagiwa', 3.05, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (17, 5, 'Yamagiwa II', 3.05, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (18, 5, 'Miyabi', 1.21, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (19, 5, 'Yamagiwa+Miyabi', 4.25, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (20, 5, 'Yamagiwa+Miyabi II', 4.25, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (21, 6, 'Windmills', 2.06, 2);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (22, 6, 'Windmills II', 2.06, 2);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (23, 6, 'Road Track - A', 3.18, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (24, 6, 'Road Track - A II', 3.18, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (25, 6, 'Road Track - B', 2.42, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (26, 6, 'Road Track - B II', 2.42, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (27, 6, 'Road Track.- C', 1.65, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (28, 6, 'Road Track -C II', 1.65, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (29, 7, 'Default', 1.99, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (30, 7, 'II', 1.99, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (31, 7, 'Infield A', 2.08, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (32, 7, 'Infield A II', 2.08, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (33, 7, 'Infield B', 1.78, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (34, 7, 'Infield B II', 1.78, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (35, 8, 'Default', 1.27, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (36, 9, 'Grand Prix Circuit', 2.45, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (37, 9, 'Indy Circuit', 1.21, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (38, 10, 'Central Outer Loop', 2.74, 4);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (39, 10, 'Central Inner Loop', 2.72, 4);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (40, 10, 'East Outer Loop', 4.54, 4);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (41, 10, 'East Inner Loop', 4.47, 4);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (42, 10, 'South Outer Loop', 3.23, 4);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (43, 10, 'South Inner Loop', 4.08, 4);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (44, 11, 'Big Willow', 2.46, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (45, 11, 'Streets of Willow Springs', 1.66, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (46, 11, 'Streets of Willow Springs II', 1.66, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (47, 11, 'Horse Thief Mile', 1.01, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (48, 11, 'Horse Thief Mill II', 1.01, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (49, 12, 'Default', 1.04, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (50, 12, 'II', 1.04, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (51, 13, 'Default', 3.61, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (52, 13, 'East Course', 1.39, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (53, 14, 'Default', 2.9, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (54, 14, 'Shortcut Course', 1.88, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (55, 15, 'Grand Prix Layout', 2.89, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (56, 16, 'A', 5.89, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (57, 16, 'A II', 5.89, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (58, 16, 'B', 4.39, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (59, 16, 'B II', 4.39, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (60, 16, 'C', 6.73, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (61, 16, 'C II', 6.73, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (62, 17, 'Default', 3.37, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (63, 17, 'II', 3.37, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (64, 18, 'Default', 3.6, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (65, 18, 'No Chicane', 3.58, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (66, 19, 'Default', 2.37, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (67, 20, 'Default', 3.86, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (68, 21, 'Default', 2.68, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (69, 21, 'Short Track', 1.45, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (70, 22, 'Default', 18.82, 1);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (71, 23, 'Default', 4.28, 2);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (72, 23, 'II', 4.28, 2);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (73, 24, 'Default', 4.35, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (74, 25, 'Default', 8.47, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (75, 25, 'No Chicane', 8.43, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (76, 26, 'Default', 2.68, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (77, 27, 'Default', 2.84, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (78, 27, '(Short)', 2.81, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (79, 28, 'Nordschleife', 12.95, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (80, 28, '24h', 15.77, 3);
INSERT INTO track_layout (id, track_id, name, miles, circuit_id) VALUES (81, 28, 'GP', 3.2, 3);

-- Table: race_collection

INSERT INTO race_collection (id, league_id, name, description) VALUES (1, 2, 'Sunday Cup', 'The grassroots introduction to racing. No restrictions on car models.');
INSERT INTO race_collection (id, league_id, name, description) VALUES (2, 1, 'Clubman Cup', 'An event for beginners just getting the hang of racing. No restrctions on car models.');
INSERT INTO race_collection (id, league_id, name, description) VALUES (3, 2, 'FF Challenge', 'Master Front wheel drive sports cars with understeer.');

PRAGMA foreign_keys = on;
