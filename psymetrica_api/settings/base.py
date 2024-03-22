from datetime import timedelta
from os import environ
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(
    environ.get(
        "SECRET_KEY",
        "django-insecure-rb!j(rv7n#=7rl0)1i-d3r$u9vowtc3y-b7m$@fl^tf1rk2n#+",
    )
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(environ.get("DEBUG", True))

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost", "192.168.0.101"]


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_yasg",
    "django_filters",
    "corsheaders",
    "djcelery_email",
    "rest_framework_simplejwt",
    "djoser",
    "rest_framework.authtoken",
    "colorfield",
]

LOCAL_APPS = [
    "apps.users",
    "apps.base",
    "apps.tests",
    "apps.scales",
    "apps.questions",
    "apps.options",
    "apps.attempts",
    "apps.notifications",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "psymetrica_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "psymetrica_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(environ.get("POSTGRES_DB", "psymetrica")),
        "USER": str(environ.get("POSTGRES_USER", "root")),
        "PASSWORD": str(environ.get("POSTGRES_PASSWORD", "root")),
        "HOST": str(environ.get("POSTGRES_HOST", "localhost")),
        "PORT": str(environ.get("POSTGRES_PORT", "5432")),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# argon passwd hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_USER_MODEL = "users.user"

# localtization
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Asia/Irkutsk"

USE_I18N = True

USE_TZ = True

# static and media files
STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

CORS_URLS_REGEX = r"^/api/.*$"

SITE_ID = 1


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# custom logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django.request": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {name} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        }
    },
}


CELERY_BROKER_URL = environ.get("CELERY_BROKER")
CELERY_RESULT_BACKEND = environ.get("CELERY_BACKEND")
CELERY_TIMEZONE = "Asia/Irkutsk"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": environ.get("JWT_SIGNING_KEY", "secret_key"),
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
}

DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "email",
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "SERIALIZERS": {
        "user_create": "apps.users.serializers.CreateUserSerializer",
        "user": "apps.users.serializers.UserSerializer",
        "current_user": "apps.users.serializers.UserSerializer",
    },
}

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]


# настройки логики/работы самого приложения
APP_SETTINGS = {
    # время между ответами в секундах, после которого будет считатся, что пользователь прервал тест.
    "TIME_TO_ATTEMPT_PAUSE": 300,
}
