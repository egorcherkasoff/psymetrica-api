#!/bin/bash

set -o errexit
set -o pipefall
set -o nounset

python manage.py collectstatic --noinput

python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000