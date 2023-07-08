from .base import *

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = environ.get("EMAIL_HOST", "mailhog")
EMAIL_PORT = environ.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "psymetrica@ya.ru"
DOMAIN = environ.get("DOMAIN")
SITE_NAME = "Psymetrica"
