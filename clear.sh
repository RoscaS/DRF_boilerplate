#!/usr/bin/env bash

# DB ------
dbuser="drftest";
dbname="drftest";
password="drftest";

echo "Step 0: clearing";
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/media/*"  -delete
echo Migration files deleted.
rm db.sqlite3
echo database deleted.

echo "Step 1: Droping database & user";
psql postgres -c "DROP DATABASE IF EXISTS $dbname";
psql postgres -c "DROP USER IF EXISTS $dbuser";

echo "Step 2: Creating new user and database";
psql postgres -c "CREATE USER $dbuser WITH ENCRYPTED PASSWORD '$password'";
psql postgres -c "CREATE DATABASE $dbname";
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $dbname TO $dbuser";
psql postgres -c "GRANT $dbuser TO $USER";

# Initialization ------

python manage.py makemigrations
python manage.py migrate

# Mock data ------
python manage.py create_admin
python manage.py create_user
python manage.py create_articles
python manage.py create_sections
python manage.py create_examples