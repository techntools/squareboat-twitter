#!/usr/bin/env bash

# Abort on any error (including if wait-for-it fails).
set -e

wait-for-it db:3306 --strict

python manage.py migrate
python manage.py runserver 0:8000
