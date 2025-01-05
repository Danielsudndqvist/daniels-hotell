import json
import os
import sys
from pathlib import Path

import dj_database_url
import environ
from google.oauth2 import service_account

# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = [
    ".herokuapp.com",
    "localhost",
    "127.0.0.1",
    "8000-danielsudnd-danielshote-yxqlj3w7p5e.ws.codeinstitute-ide.net",
    "daniels-hotel-64602c2a7743.herokuapp.com",
    ".gitpod.io",
]

PYTEST_SETTINGS = {
    "DJANGO_SETTINGS_MODULE": "daniels-hotell.settings",
}

# Application definition
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

ROOT_URLCONF = "daniels-hotell.urls"

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

WSGI_APPLICATION = "daniels-hotell.wsgi.application"

LOGIN_URL = "login"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Database configuration for Heroku
if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True,
    )

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Google Cloud Storage settings
IS_DEVELOPMENT = env("DJANGO_ENV", default="development") == "development"
GS_BUCKET_NAME = env("GS_BUCKET_NAME", default=None)

if IS_DEVELOPMENT:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    GS_CREDENTIALS = None
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        )
    elif "GOOGLE_CREDENTIALS" in os.environ:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
            json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
        )

    if GS_CREDENTIALS:
        STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        DEFAULT_FILE_STORAGE = "rooms.custom_storage.GoogleCloudMediaFileStorage"
        STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

        # Additional GCS settings
        GS_DEFAULT_ACL = None
        GS_FILE_OVERWRITE = False
    else:
        STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
        DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "rooms.CustomUser"

CSRF_TRUSTED_ORIGINS = [
    "https://*.herokuapp.com",
    "https://*.gitpod.io",
    "https://*.codeinstitute-ide.net",
]

# Email configuration (update as needed)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Production security settings
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Logging configuration
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

# Heroku settings
if "DYNO" in os.environ:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True

# Print debug information
if DEBUG:
    print(f"IS_DEVELOPMENT: {IS_DEVELOPMENT}")
    print(f"STATIC_URL: {STATIC_URL}")
    print(f"STATICFILES_DIRS: {STATICFILES_DIRS}")

# HTML Validator Settings
HTMLVALIDATOR_ENABLED = True
HTMLVALIDATOR_OUTPUT = 'stdout'  # Output to console
HTMLVALIDATOR_FAILFAST = False  # Don't stop on first error
HTMLVALIDATOR_VNU_URL = 'http://localhost:8888'  # Default VNU server URL
