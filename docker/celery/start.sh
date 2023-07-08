#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
watchmedo auto-restart -d psymetrica_api/ -p '*.py' -- celery -A psymetrica_api worker --loglevel=info