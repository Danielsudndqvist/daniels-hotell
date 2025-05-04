import json
import os
import sys
from pathlib import Path

import dj_database_url
import environ
from google.oauth2 import service_account

# Removed unused imports:
# from django.core.exceptions import ImproperlyConfigured
# from storages.backends.gcloud import GoogleCloudStorage
# from storages.utils import setting
# from urllib.parse import urljoin


# Environment and Base Configuration
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Security Settings
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=False)

# Hosts and Security
ALLOWED_HOSTS = [
    ".herokuapp.com",
    "localhost",
    "127.0.0.1",
    ".gitpod.io",
    "daniels-hotel-64602c2a7743.herokuapp.com",
    "8000-danielsudnd-danielshote-6uv7tjrhsr1.ws.codeinstitute-ide.net",
]

# Application Definition
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

# URLs and WSGI Configuration
ROOT_URLCONF = "daniels-hotell.urls"
WSGI_APPLICATION = "daniels-hotell.wsgi.application"

# Database Configuration
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600,
    ),
}

# Testing Database Configuration
if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }

# Static and Media Files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Google Cloud Storage Configuration - with Debug Logging
IS_DEVELOPMENT = env("DJANGO_ENV", default="development") == "development"
print(f"DJANGO_ENV from env: {env('DJANGO_ENV', default='development')}")
print(f"IS_DEVELOPMENT calculated value: {IS_DEVELOPMENT}")

GS_BUCKET_NAME = env("GS_BUCKET_NAME", default=None)
print(f"GS_BUCKET_NAME from env: {GS_BUCKET_NAME}")
print(f"GS_BUCKET_NAME from os.environ: {os.environ.get('GS_BUCKET_NAME')}")

# Fallback to os.environ if env() doesn't work
if GS_BUCKET_NAME is None and "GS_BUCKET_NAME" in os.environ:
    GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
    print(f"Using GS_BUCKET_NAME from os.environ directly: {GS_BUCKET_NAME}")

print(f"DYNO in os.environ: {'DYNO' in os.environ}")

if not IS_DEVELOPMENT and GS_BUCKET_NAME:
    try:
        # Credentials handling
        GS_CREDENTIALS = None
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            print("Using GOOGLE_APPLICATION_CREDENTIALS")
            GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            )
        elif "GOOGLE_CREDENTIALS" in os.environ:
            print("Using GOOGLE_CREDENTIALS")
            GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
                json.loads(os.environ["GOOGLE_CREDENTIALS"])
            )

        # Only set storage if credentials are found
        if GS_CREDENTIALS:
            print("GS_CREDENTIALS found, configuring storage backends")
            DEFAULT_FILE_STORAGE = "rooms.storage.GoogleCloudMediaFileStorage"
            MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
            STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
            STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

            GS_DEFAULT_ACL = "publicRead"
            GS_FILE_OVERWRITE = False

            print(f"Storage configuration complete:")
            print(f"DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")
            print(f"MEDIA_URL: {MEDIA_URL}")
        else:
            print("No GS_CREDENTIALS found")

    except Exception as e:
        print(f"Google Cloud Storage configuration error: {e}")
        # Fallback to default storage if GCS setup fails
        DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
        print("Falling back to FileSystemStorage")


# Production Security Settings
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Custom User Model
AUTH_USER_MODEL = "rooms.CustomUser"

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://*.herokuapp.com",
    "https://*.gitpod.io",
    "https://*.ws.codeinstitute-ide.net",
]

# Defaults
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# In your logging configuration
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
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "storages": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "google.cloud": {  # Add this for GCS debugging
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}


# Template Configuration
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

# Heroku-Specific Settings
if "DYNO" in os.environ:
    print("Running on Heroku, applying Heroku-specific settings")
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True

    # Explicitly check GCS configuration when on Heroku
    print("Checking GCS configuration on Heroku...")
    if "GS_BUCKET_NAME" in os.environ and "GOOGLE_CREDENTIALS" in os.environ:
        try:
            print(
                f"GS_BUCKET_NAME from os.environ on Heroku: {os.environ.get('GS_BUCKET_NAME')}"
            )
            GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
            GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
                json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
            )

            DEFAULT_FILE_STORAGE = "rooms.storage.GoogleCloudMediaFileStorage"
            MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
            STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
            STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

            GS_DEFAULT_ACL = "publicRead"
            GS_FILE_OVERWRITE = False

            print("Successfully configured GCS on Heroku!")
            print(f"DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")
            print(f"MEDIA_URL: {MEDIA_URL}")
        except Exception as e:
            print(f"Error configuring GCS on Heroku: {e}")
    else:
        missing = []
        if "GS_BUCKET_NAME" not in os.environ:
            missing.append("GS_BUCKET_NAME")
        if "GOOGLE_CREDENTIALS" not in os.environ:
            missing.append("GOOGLE_CREDENTIALS")
        print(f"Missing Heroku config vars: {', '.join(missing)}")
