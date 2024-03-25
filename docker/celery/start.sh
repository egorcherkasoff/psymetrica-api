#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
celery -A psymetrica_api worker --loglevel=info