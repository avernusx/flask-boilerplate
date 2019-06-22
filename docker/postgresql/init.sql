-- Modify template database
-- pgcrypto allow to use gen_random_uuid()
\c template1;
CREATE EXTENSION if not exists pgcrypto;
CREATE EXTENSION if not exists hstore;
CREATE DATABASE site;
CREATE USER docker with superuser password 'docker';
GRANT ALL privileges ON DATABASE site TO docker;
