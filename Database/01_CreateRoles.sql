\set db_name `echo "$POSTGRES_DB"`
\set schema_name `echo "$SCHEMA_DB"`

\set pg_pass `echo "$POSTGRES_PASSWORD"`
\set load_pass `echo "$DB_ROLE_LOAD_DATA_PASS"`
\set read_pass `echo "$DB_ROLE_READ_DATA_PASS"`

ALTER USER authenticator WITH PASSWORD :'pg_pass';
CREATE ROLE loader_data WITH LOGIN PASSWORD :'load_pass';
CREATE ROLE reader_data WITH LOGIN PASSWORD :'read_pass';

GRANT loader_data TO authenticator;
GRANT reader_data TO authenticator;

GRANT CONNECT ON DATABASE :"db_name" TO loader_data, reader_data, authenticator;
GRANT USAGE ON SCHEMA :"schema_name" TO loader_data, reader_data, authenticator;

GRANT INSERT , SELECT  ON ALL TABLES IN SCHEMA :"schema_name" TO loader_data;
GRANT USAGE , SELECT ON ALL SEQUENCES IN SCHEMA :"schema_name" TO loader_data;
GRANT SELECT ON ALL TABLES IN SCHEMA :"schema_name" TO reader_data;

ALTER DEFAULT PRIVILEGES IN SCHEMA :"schema_name" 
    GRANT INSERT , SELECT ON TABLES TO loader_data;
ALTER DEFAULT PRIVILEGES IN SCHEMA :"schema_name" 
    GRANT USAGE , SELECT ON SEQUENCES TO loader_data;
ALTER DEFAULT PRIVILEGES IN SCHEMA :"schema_name" 
    GRANT SELECT ON TABLES TO reader_data;