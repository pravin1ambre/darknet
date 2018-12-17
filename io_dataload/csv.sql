 CREATE TABLE dataload (
    date VARCHAR(30) NOT NULL,
    unix_timestamp VARCHAR(30) NOT NULL,
    metrics VARCHAR(30)  NULL,
    value VARCHAR(30)  NULL,
    date_time TIMESTAMP
 )

 CREATE TABLE maptable (
    types VARCHAR(30) NOT NULL,
    name VARCHAR(30) NOT NULL,
    metrics VARCHAR(30) NOT NULL UNIQUE,
 )