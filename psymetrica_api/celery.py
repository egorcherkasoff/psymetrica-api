from os import environ

from celery import Celery
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

environ.setdefault("DJANGO_SETTINGS_MODULE", "psymetrica_api.settings.local")

app = Celery("psymetrica_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
