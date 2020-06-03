#!/usr/bin/env bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/media/*"  -delete
echo Migration files deleted.
rm db.sqlite3
echo database deleted.

python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
python manage.py create_user
python manage.py create_articles
python manage.py create_sections
python manage.py create_examples
