--
-- File generated with SQLiteStudio v3.2.1 on Sat Dec 7 13:44:01 2019
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
-- Table: category
INSERT INTO category (id, name, description, sortOrder) VALUES (1, 'Gr.1', 'Racing cars with bodies and engines specially developed to provide higher performance. This group also includes prototype sports cars etc.', 10);
INSERT INTO category (id, name, description, sortOrder) VALUES (2, 'Gr.2', 'Racing cars that represent the highest peak of the touring car category. This group corresponds to the GT500 class that runs in the Japanese SUPER GT.', 20);
INSERT INTO category (id, name, description, sortOrder) VALUES (3, 'Gr.3', 'Racing cars with special bodywork for greater aerodynamic performance. This group corresponds to the FIA''s GT3 class.', 30);
INSERT INTO category (id, name, description, sortOrder) VALUES (4, 'Gr.4', 'Racing cars with basic performance enhancements, such as additional safety equipment or weight optimization. This group corresponds to the FIA''s GT4 class.', 40);
INSERT INTO category (id, name, description, sortOrder) VALUES (5, 'Gr.B', 'Rally cars that have been modified for dirt racing, with improved suspension systems, body height control, and so on.', 50);
INSERT INTO category (id, name, description, sortOrder) VALUES (6, 'Gr.X', 'Extreme cars that don''t fit into any racing category.', 60);
INSERT INTO category (id, name, description, sortOrder) VALUES (7, 'N100', 'Power level 0 to 150 PS (148 hp; 110 kW)', 100);
INSERT INTO category (id, name, description, sortOrder) VALUES (8, 'N200', 'Power level 150 PS (148 hp; 110 kW) to 250 PS (247 hp; 184 kW)', 200);
INSERT INTO category (id, name, description, sortOrder) VALUES (9, 'N300', 'Power level 251 PS (248 hp; 185 kW) to 350 PS (345 hp; 257 kW)', 300);
INSERT INTO category (id, name, description, sortOrder) VALUES (10, 'N400', 'Power level 351 PS (346 hp; 258 kW) to 450 PS (444 hp; 331 kW)', 400);
INSERT INTO category (id, name, description, sortOrder) VALUES (11, 'N500', 'Power level 451 PS (445 hp; 332 kW) to 550 PS (542 hp; 405 kW)', 500);
INSERT INTO category (id, name, description, sortOrder) VALUES (12, 'N600', 'Power level 551 PS (543 hp; 405 kW) to 650 PS (641 hp; 478 kW)', 600);
INSERT INTO category (id, name, description, sortOrder) VALUES (13, 'N700', 'Power level 651 PS (642 hp; 479 kW) to 750 PS (740 hp; 552 kW)', 700);
INSERT INTO category (id, name, description, sortOrder) VALUES (14, 'N800', 'Power level 751 PS (741 hp; 552 kW) to 850 PS (838 hp; 625 kW)', 800);
INSERT INTO category (id, name, description, sortOrder) VALUES (15, 'N900', 'Power level 851 PS (839 hp; 626 kW) to 950 PS (937 hp; 699 kW)', 900);
INSERT INTO category (id, name, description, sortOrder) VALUES (16, 'N1000', 'Power level 951 PS (938 hp; 699 kW) to Infinite', 1000);

-- Table: circuit
INSERT INTO circuit (id, name) VALUES (1, 'Original Circuit');
INSERT INTO circuit (id, name) VALUES (2, 'Dirt / Snow');
INSERT INTO circuit (id, name) VALUES (3, 'World Circuit');
INSERT INTO circuit (id, name) VALUES (4, 'City Circuit');

-- Table: country
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (1, 'Afghanistan', 'AF', 'AFG', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (2, 'Aland Islands', 'AX', 'ALA', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (3, 'Albania', 'AL', 'ALB', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (4, 'Algeria', 'DZ', 'DZA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (5, 'American Samoa', 'AS', 'ASM', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (6, 'Andorra', 'AD', 'AND', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (7, 'Angola', 'AO', 'AGO', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (8, 'Anguilla', 'AI', 'AIA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (9, 'Antarctica', 'AQ', 'ATA', '');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (10, 'Antigua and Barbuda', 'AG', 'ATG', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (11, 'Argentina', 'AR', 'ARG', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (12, 'Armenia', 'AM', 'ARM', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (13, 'Aruba', 'AW', 'ABW', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (14, 'Australia', 'AU', 'AUS', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (15, 'Austria', 'AT', 'AUT', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (16, 'Azerbaijan', 'AZ', 'AZE', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (17, 'Bahamas', 'BS', 'BHS', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (18, 'Bahrain', 'BH', 'BHR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (19, 'Bangladesh', 'BD', 'BGD', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (20, 'Barbados', 'BB', 'BRB', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (21, 'Belarus', 'BY', 'BLR', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (22, 'Belgium', 'BE', 'BEL', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (23, 'Belize', 'BZ', 'BLZ', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (24, 'Benin', 'BJ', 'BEN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (25, 'Bermuda', 'BM', 'BMU', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (26, 'Bhutan', 'BT', 'BTN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (27, 'Bolivia (Plurinational State of)', 'BO', 'BOL', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (28, 'Bonaire, Sint Eustatius and Saba', 'BQ', 'BES', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (29, 'Bosnia and Herzegovina', 'BA', 'BIH', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (30, 'Botswana', 'BW', 'BWA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (31, 'Bouvet Island', 'BV', 'BVT', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (32, 'Brazil', 'BR', 'BRA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (33, 'British Indian Ocean Territory', 'IO', 'IOT', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (34, 'Brunei Darussalam', 'BN', 'BRN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (35, 'Bulgaria', 'BG', 'BGR', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (36, 'Burkina Faso', 'BF', 'BFA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (37, 'Burundi', 'BI', 'BDI', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (38, 'C+�te d''Ivoire', 'CI', 'CIV', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (39, 'Cabo Verde', 'CV', 'CPV', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (40, 'Cambodia', 'KH', 'KHM', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (41, 'Cameroon', 'CM', 'CMR', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (42, 'Canada', 'CA', 'CAN', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (43, 'Cayman Islands', 'KY', 'CYM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (44, 'Central African Republic', 'CF', 'CAF', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (45, 'Chad', 'TD', 'TCD', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (46, 'Chile', 'CL', 'CHL', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (47, 'China', 'CN', 'CHN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (48, 'Christmas Island', 'CX', 'CXR', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (49, 'Cocos (Keeling) Islands', 'CC', 'CCK', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (50, 'Colombia', 'CO', 'COL', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (51, 'Comoros', 'KM', 'COM', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (52, 'Congo', 'CG', 'COG', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (53, 'Congo, Democratic Republic of the', 'CD', 'COD', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (54, 'Cook Islands', 'CK', 'COK', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (55, 'Costa Rica', 'CR', 'CRI', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (56, 'Croatia', 'HR', 'HRV', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (57, 'Cuba', 'CU', 'CUB', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (58, 'Cura+�ao', 'CW', 'CUW', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (59, 'Cyprus', 'CY', 'CYP', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (60, 'Czechia', 'CZ', 'CZE', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (61, 'Denmark', 'DK', 'DNK', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (62, 'Djibouti', 'DJ', 'DJI', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (63, 'Dominica', 'DM', 'DMA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (64, 'Dominican Republic', 'DO', 'DOM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (65, 'Ecuador', 'EC', 'ECU', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (66, 'Egypt', 'EG', 'EGY', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (67, 'El Salvador', 'SV', 'SLV', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (68, 'Equatorial Guinea', 'GQ', 'GNQ', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (69, 'Eritrea', 'ER', 'ERI', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (70, 'Estonia', 'EE', 'EST', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (71, 'Eswatini', 'SZ', 'SWZ', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (72, 'Ethiopia', 'ET', 'ETH', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (73, 'Falkland Islands (Malvinas)', 'FK', 'FLK', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (74, 'Faroe Islands', 'FO', 'FRO', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (75, 'Fiji', 'FJ', 'FJI', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (76, 'Finland', 'FI', 'FIN', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (77, 'France', 'FR', 'FRA', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (78, 'French Guiana', 'GF', 'GUF', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (79, 'French Polynesia', 'PF', 'PYF', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (80, 'French Southern Territories', 'TF', 'ATF', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (81, 'Gabon', 'GA', 'GAB', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (82, 'Gambia', 'GM', 'GMB', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (83, 'Georgia', 'GE', 'GEO', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (84, 'Germany', 'DE', 'DEU', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (85, 'Ghana', 'GH', 'GHA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (86, 'Gibraltar', 'GI', 'GIB', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (87, 'Greece', 'GR', 'GRC', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (88, 'Greenland', 'GL', 'GRL', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (89, 'Grenada', 'GD', 'GRD', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (90, 'Guadeloupe', 'GP', 'GLP', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (91, 'Guam', 'GU', 'GUM', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (92, 'Guatemala', 'GT', 'GTM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (93, 'Guernsey', 'GG', 'GGY', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (94, 'Guinea', 'GN', 'GIN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (95, 'Guinea-Bissau', 'GW', 'GNB', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (96, 'Guyana', 'GY', 'GUY', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (97, 'Haiti', 'HT', 'HTI', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (98, 'Heard Island and McDonald Islands', 'HM', 'HMD', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (99, 'Holy See', 'VA', 'VAT', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (100, 'Honduras', 'HN', 'HND', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (101, 'Hong Kong', 'HK', 'HKG', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (102, 'Hungary', 'HU', 'HUN', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (103, 'Iceland', 'IS', 'ISL', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (104, 'India', 'IN', 'IND', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (105, 'Indonesia', 'ID', 'IDN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (106, 'Iran (Islamic Republic of)', 'IR', 'IRN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (107, 'Iraq', 'IQ', 'IRQ', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (108, 'Ireland', 'IE', 'IRL', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (109, 'Isle of Man', 'IM', 'IMN', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (110, 'Israel', 'IL', 'ISR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (111, 'Italy', 'IT', 'ITA', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (112, 'Jamaica', 'JM', 'JAM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (113, 'Japan', 'JP', 'JPN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (114, 'Jersey', 'JE', 'JEY', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (115, 'Jordan', 'JO', 'JOR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (116, 'Kazakhstan', 'KZ', 'KAZ', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (117, 'Kenya', 'KE', 'KEN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (118, 'Kiribati', 'KI', 'KIR', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (119, 'Korea (Democratic People''s Republic of)', 'KP', 'PRK', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (120, 'Korea, Republic of', 'KR', 'KOR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (121, 'Kuwait', 'KW', 'KWT', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (122, 'Kyrgyzstan', 'KG', 'KGZ', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (123, 'Lao People''s Democratic Republic', 'LA', 'LAO', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (124, 'Latvia', 'LV', 'LVA', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (125, 'Lebanon', 'LB', 'LBN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (126, 'Lesotho', 'LS', 'LSO', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (127, 'Liberia', 'LR', 'LBR', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (128, 'Libya', 'LY', 'LBY', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (129, 'Liechtenstein', 'LI', 'LIE', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (130, 'Lithuania', 'LT', 'LTU', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (131, 'Luxembourg', 'LU', 'LUX', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (132, 'Macao', 'MO', 'MAC', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (133, 'Madagascar', 'MG', 'MDG', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (134, 'Malawi', 'MW', 'MWI', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (135, 'Malaysia', 'MY', 'MYS', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (136, 'Maldives', 'MV', 'MDV', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (137, 'Mali', 'ML', 'MLI', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (138, 'Malta', 'MT', 'MLT', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (139, 'Marshall Islands', 'MH', 'MHL', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (140, 'Martinique', 'MQ', 'MTQ', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (141, 'Mauritania', 'MR', 'MRT', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (142, 'Mauritius', 'MU', 'MUS', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (143, 'Mayotte', 'YT', 'MYT', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (144, 'Mexico', 'MX', 'MEX', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (145, 'Micronesia (Federated States of)', 'FM', 'FSM', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (146, 'Moldova, Republic of', 'MD', 'MDA', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (147, 'Monaco', 'MC', 'MCO', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (148, 'Mongolia', 'MN', 'MNG', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (149, 'Montenegro', 'ME', 'MNE', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (150, 'Montserrat', 'MS', 'MSR', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (151, 'Morocco', 'MA', 'MAR', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (152, 'Mozambique', 'MZ', 'MOZ', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (153, 'Myanmar', 'MM', 'MMR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (154, 'Namibia', 'NA', 'NAM', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (155, 'Nauru', 'NR', 'NRU', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (156, 'Nepal', 'NP', 'NPL', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (157, 'Netherlands', 'NL', 'NLD', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (158, 'New Caledonia', 'NC', 'NCL', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (159, 'New Zealand', 'NZ', 'NZL', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (160, 'Nicaragua', 'NI', 'NIC', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (161, 'Niger', 'NE', 'NER', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (162, 'Nigeria', 'NG', 'NGA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (163, 'Niue', 'NU', 'NIU', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (164, 'Norfolk Island', 'NF', 'NFK', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (165, 'North Macedonia', 'MK', 'MKD', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (166, 'Northern Mariana Islands', 'MP', 'MNP', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (167, 'Norway', 'NO', 'NOR', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (168, 'Oman', 'OM', 'OMN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (169, 'Pakistan', 'PK', 'PAK', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (170, 'Palau', 'PW', 'PLW', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (171, 'Palestine, State of', 'PS', 'PSE', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (172, 'Panama', 'PA', 'PAN', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (173, 'Papua New Guinea', 'PG', 'PNG', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (174, 'Paraguay', 'PY', 'PRY', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (175, 'Peru', 'PE', 'PER', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (176, 'Philippines', 'PH', 'PHL', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (177, 'Pitcairn', 'PN', 'PCN', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (178, 'Poland', 'PL', 'POL', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (179, 'Portugal', 'PT', 'PRT', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (180, 'Puerto Rico', 'PR', 'PRI', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (181, 'Qatar', 'QA', 'QAT', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (182, 'R+�union', 'RE', 'REU', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (183, 'Romania', 'RO', 'ROU', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (184, 'Russian Federation', 'RU', 'RUS', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (185, 'Rwanda', 'RW', 'RWA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (186, 'Saint Barth+�lemy', 'BL', 'BLM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (187, 'Saint Helena, Ascension and Tristan da Cunha', 'SH', 'SHN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (188, 'Saint Kitts and Nevis', 'KN', 'KNA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (189, 'Saint Lucia', 'LC', 'LCA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (190, 'Saint Martin (French part)', 'MF', 'MAF', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (191, 'Saint Pierre and Miquelon', 'PM', 'SPM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (192, 'Saint Vincent and the Grenadines', 'VC', 'VCT', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (193, 'Samoa', 'WS', 'WSM', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (194, 'San Marino', 'SM', 'SMR', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (195, 'Sao Tome and Principe', 'ST', 'STP', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (196, 'Saudi Arabia', 'SA', 'SAU', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (197, 'Senegal', 'SN', 'SEN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (198, 'Serbia', 'RS', 'SRB', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (199, 'Seychelles', 'SC', 'SYC', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (200, 'Sierra Leone', 'SL', 'SLE', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (201, 'Singapore', 'SG', 'SGP', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (202, 'Sint Maarten (Dutch part)', 'SX', 'SXM', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (203, 'Slovakia', 'SK', 'SVK', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (204, 'Slovenia', 'SI', 'SVN', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (205, 'Solomon Islands', 'SB', 'SLB', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (206, 'Somalia', 'SO', 'SOM', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (207, 'South Africa', 'ZA', 'ZAF', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (208, 'South Georgia and the South Sandwich Islands', 'GS', 'SGS', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (209, 'South Sudan', 'SS', 'SSD', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (210, 'Spain', 'ES', 'ESP', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (211, 'Sri Lanka', 'LK', 'LKA', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (212, 'Sudan', 'SD', 'SDN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (213, 'Suriname', 'SR', 'SUR', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (214, 'Svalbard and Jan Mayen', 'SJ', 'SJM', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (215, 'Sweden', 'SE', 'SWE', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (216, 'Switzerland', 'CH', 'CHE', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (217, 'Syrian Arab Republic', 'SY', 'SYR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (218, 'Taiwan, Province of China', 'TW', 'TWN', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (219, 'Tajikistan', 'TJ', 'TJK', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (220, 'Tanzania, United Republic of', 'TZ', 'TZA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (221, 'Thailand', 'TH', 'THA', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (222, 'Timor-Leste', 'TL', 'TLS', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (223, 'Togo', 'TG', 'TGO', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (224, 'Tokelau', 'TK', 'TKL', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (225, 'Tonga', 'TO', 'TON', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (226, 'Trinidad and Tobago', 'TT', 'TTO', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (227, 'Tunisia', 'TN', 'TUN', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (228, 'Turkey', 'TR', 'TUR', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (229, 'Turkmenistan', 'TM', 'TKM', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (230, 'Turks and Caicos Islands', 'TC', 'TCA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (231, 'Tuvalu', 'TV', 'TUV', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (232, 'Uganda', 'UG', 'UGA', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (233, 'Ukraine', 'UA', 'UKR', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (234, 'United Arab Emirates', 'AE', 'ARE', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (235, 'United Kingdom of Great Britain and Northern Ireland', 'GB', 'GBR', 'Europe');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (236, 'United States Minor Outlying Islands', 'UM', 'UMI', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (237, 'United States of America', 'US', 'USA', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (238, 'Uruguay', 'UY', 'URY', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (239, 'Uzbekistan', 'UZ', 'UZB', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (240, 'Vanuatu', 'VU', 'VUT', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (241, 'Venezuela (Bolivarian Republic of)', 'VE', 'VEN', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (242, 'Viet Nam', 'VN', 'VNM', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (243, 'Virgin Islands (British)', 'VG', 'VGB', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (244, 'Virgin Islands (U.S.)', 'VI', 'VIR', 'Americas');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (245, 'Wallis and Futuna', 'WF', 'WLF', 'Oceania');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (246, 'Western Sahara', 'EH', 'ESH', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (247, 'Yemen', 'YE', 'YEM', 'Asia');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (248, 'Zambia', 'ZM', 'ZMB', 'Africa');
INSERT INTO country (ID, name, alpha2, alpha3, region) VALUES (249, 'Zimbabwe', 'ZW', 'ZWE', 'Africa');

-- Table: drivetrain

INSERT INTO drivetrain (id, code, description) VALUES (1, 'FF', 'Front Engine, Front wheel drive');
INSERT INTO drivetrain (id, code, description) VALUES (2, 'FR', 'Front Engine, Rear wheel drive');
INSERT INTO drivetrain (id, code, description) VALUES (3, 'MR', 'Middle Engine, Rear wheel drive');
INSERT INTO drivetrain (id, code, description) VALUES (4, '4WD', 'Four wheel drive');
INSERT INTO drivetrain (id, code, description) VALUES (5, 'RR', 'Rear Engine (behind the rear axle) Rear wheel drive');

-- Table: league
INSERT INTO league (id, name, sortord) VALUES (1, 'Amateur', 10);
INSERT INTO league (id, name, sortord) VALUES (2, 'Beginner', 1);
INSERT INTO league (id, name, sortord) VALUES (3, 'Endurance', 30);
INSERT INTO league (id, name, sortord) VALUES (4, 'Professional', 20);

-- Table: race_type
INSERT INTO race_type (ID, name) VALUES (1, 'Lap');
INSERT INTO race_type (ID, name) VALUES (2, 'Endurance');

-- Table: weather
INSERT INTO weather (id, name) VALUES (1, 'NA');
INSERT INTO weather (id, name) VALUES (2, 'Weather 2');

PRAGMA foreign_keys = on;
