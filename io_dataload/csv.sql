 CREATE TABLE dataload (
 date VARCHAR(30) NOT NULL,
 unix_timestamp VARCHAR(30) NOT NULL,
 metrics INT NOT NULL,
 value float NOT NULL,
 date_time TIMESTAMP
 )

 CREATE TABLE maptable (
 types VARCHAR(30) NOT NULL,
 name VARCHAR(30) NOT NULL,
 metrics VARCHAR(30) NOT NULL UNIQUE,
 )