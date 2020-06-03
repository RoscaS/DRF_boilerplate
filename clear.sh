#!/usr/bin/env bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/media/*"  -delete
echo Migration files deleted.
rm db.sqlite3
echo database deleted.

python manage.py makemigrations
python manage.py migrate
python manage.py createadmin
python manage.py createuser
python manage.py createarticles
