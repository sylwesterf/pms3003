CREATE TABLE db_pms3003.fct_pm
(
pm1 int NOT NULL,
pm25 int NOT NULL,
pm10 int NOT NULL,
dt datetime NOT NULL
);

CREATE USER 'sa' IDENTIFIED BY 'xxx';
GRANT ALL ON * TO 'sa';

CREATE USER 'shiny' IDENTIFIED BY 'xxx';
GRANT SELECT ON db_pms3003.fct_pm TO 'shiny';

CREATE USER 'rpi' IDENTIFIED BY 'xxx';
GRANT INSERT ON db_pms3003.fct_pm TO 'rpi';
