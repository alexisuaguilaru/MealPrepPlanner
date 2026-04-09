\set db_name `echo "$POSTGRES_DB"`
\set schema_name `echo "$SCHEMA_DB"`

\set load_pass `echo "$DB_ROLE_LOAD_DATA_PASS"`
\set read_pass `echo "$DB_ROLE_READ_DATA_PASS"`

CREATE ROLE loader_data WITH LOGIN PASSWORD :'load_pass';
CREATE ROLE reader_data WITH LOGIN PASSWORD :'read_pass';

GRANT CONNECT ON DATABASE :"db_name" TO loader_data;
GRANT CONNECT ON DATABASE :"db_name" TO reader_data;

GRANT USAGE ON SCHEMA :"schema_name" TO loader_data;
GRANT USAGE ON SCHEMA :"schema_name" TO reader_data;

GRANT INSERT , SELECT  ON ALL TABLES IN SCHEMA :"schema_name" TO loader_data;
GRANT USAGE , SELECT ON ALL SEQUENCES IN SCHEMA :"schema_name" TO loader_data;
GRANT SELECT ON ALL TABLES IN SCHEMA :"schema_name" TO reader_data;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon;