#!/bin/bash

echo "CREATING DBS"

# Create the database if it doesn't exist
psql -U "$POSTGRES_USER" -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE "$ANALYTICS_DB_NAME";
EOSQL

psql -U "$POSTGRES_USER" -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE "keycloakdb";
EOSQL