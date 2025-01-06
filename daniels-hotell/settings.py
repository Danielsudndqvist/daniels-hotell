import json
import os
import sys
from pathlib import Path

import dj_database_url
import environ
from google.oauth2 import service_account

# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Secret key
SECRET_KEY = env("SECRET_KEY")

# Debug mode
DEBUG = env("DEBUG", default=False)

# Allowed hosts
ALLOWED_HOSTS = [
    ".herokuapp.com",
    "localhost",
    "127.0.0.1",
    ".gitpod.io",
    "daniels-hotel-64602c2a7743.herokuapp.com",
    "8000-danielsudnd-danielshote-yxqlj3w7p5e.ws.codeinstitute-ide.net"
]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rooms",
    "storages",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs and WSGI
ROOT_URLCONF = "daniels-hotell.urls"
WSGI_APPLICATION = "daniels-hotell.wsgi.application"

# Database configuration
DATABASES = {
    "default": dj_database_url.config(default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}", conn_max_age=600),
}

# Testing database
if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }

# Static and media files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Google Cloud Storage settings
IS_DEVELOPMENT = env("DJANGO_ENV", default="development") == "development"
GS_BUCKET_NAME = env("GS_BUCKET_NAME", default=None)

if not IS_DEVELOPMENT and GS_BUCKET_NAME:
    GS_CREDENTIALS = None
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        )
    elif "GOOGLE_CREDENTIALS" in os.environ:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
            json.loads(os.environ["GOOGLE_CREDENTIALS"])
        )

    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

    GS_DEFAULT_ACL = None
    GS_FILE_OVERWRITE = False

# Security settings for production
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Custom user model
AUTH_USER_MODEL = "rooms.CustomUser"

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://*.herokuapp.com",
    "https://*.gitpod.io",
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "google.auth": {
            "level": "DEBUG",
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

# Heroku-specific settings
if "DYNO" in os.environ:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
