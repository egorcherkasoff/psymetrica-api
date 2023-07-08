#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
celery -A psymetrica_api --broker="${CELERY_BROKER}" \
flower --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"