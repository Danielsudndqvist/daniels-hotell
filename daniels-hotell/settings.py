import os
from pathlib import Path
import environ
import dj_database_url
from google.oauth2 import service_account

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1', '8000-danielsudnd-danielshote-f9o9cx36nv8.ws.codeinstitute-ide.net']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rooms',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'daniels-hotell.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'daniels-hotell.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ... (previous settings remain the same)

# Google Cloud Storage settings
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    {
        "type": "service_account",
        "project_id": "hotel-mediafiles",
        "private_key_id": "53ce74f003b4dddef7cc21ea4419d4e21b2fafec",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCSsYqVHey+0GBv\nPMPkxq95OvpGWOjKxi21E+YrzZptCIogxwO7+fzPcddNe8B1hTDtXwJ+x4nu1DX0\nU9k/8jexmjDlLgKQxEQbzXx3hV4LVSRbgnVFVKuE9owF0iRXoJ8rvlqff+ekfny0\n42UgwExfNi6f8SxKQTTz6bkVoZjpjpT4QKiJTRA5K+onmVkkAehOZxJ2N83hR3tV\nPT04Vpp0yx6fgQ/7xebk5wCA7Aw3L7VE/09FmYiJrn+GYSfqYPgNJzcjIr+ThQmx\nTr7vf3abZCkLcrxDz0z77SDNWY9TgN41fX8Lg0YNi7i+sArO1uRvw/qIaipa2HY6\nElGXBEYHAgMBAAECggEABGs5Ck04ofYt9CaHnMnIDxCnPweTmklw/AjpleffdH8I\nMNI95bjd6YkmMVfT0CvJxwS7KFguFVXVeugsXartYY9hqgMCTHEVFM9SUK629Vlv\nEHCexA63t015TKhBXwBgJcBaA377WoRS5lyz4aeD8Bmg5ZbYEjPiT/dPk3wRhUuH\nYK91BdWTrEdGZlo9oMaEaLfOKIEPyENcKP0bzt+7B4yv9Aoe8c3cqCLFiTPuip4w\niXbpWR7vIR9jOCATrFXc1QzlzRkRQBzOhvSjgF4xnxuyKLjetVpM1aHnj6Tnbnly\ncwmv3j/PlFh7F9AG8yDoSwRYUlm+jMvPWhq3vPJKwQKBgQDNCkIPUxZyqfSbvQAC\nBqayDUygzwkS7gKEWY34Guj44YcirWuxC06Nf0/UgCugldjtfcIc34sFYCSigu1s\nXAIyA7olw4rnnwtbU3OEvNFQQKXZotKvi+uKHMjXnEetnrTQnbewFV0Cal/KjKE5\nC6LH0Ll0s8HH5Pu+W456dd9rxwKBgQC3JvcB0lnHLqh9TIoVmufzPybop5CN9ERI\ne1un7fZSMw/VNU9yGQPFSWU/EYbxVx0C/4ZQizyfYX23TEqAIhZDdyT84qWQyIea\nYl+cA+g5VZR/owS1RFOaa/sh2cKIShyn7f0mC+lh5W19NekzhGqKz8JmtHfbGJnO\n8NrfaEnTwQKBgAY11lRift6QOUFyUwq8qtXfwz9npe212cuqbrtiDUZkhlRNjmJ5\nZjKw9XkJPMkLYNuooHWBa9OI2vM1Jf3PN53OMRgtuQpU7eIhP/F4Spq0qpFR9jGs\n+kBfqNGnASDIGs/qxwKFUyDcmfQnmEaDDLYio0temnL0g497dHBPG6pHAoGAH3H9\nLr7i0yPbocemXZc/A7BwCbnbQ8QQhTFIx0g/5lUF/uEsRrasww6a530m4gDG5mDg\nuqttOSAP6YybrewsTmECZLi1HGqRfZwuNiclk9JxsIhYopaclAK+F02/7I5s5Rgj\nQokBBOHTLpA2/bVaZYLOKbwKZ/+NSM5phbnuEwECgYA/WLd3B5iJ1JOZhJDmnA0O\niqrIzSS97AQNtwSI7wSvbPXx6rNFN7UphS8/tp+0WkqgbCYsCEtsGGCdenpHka3W\nC7t0W7/XpXgs5SLqB/VW9ff1R9TMYLSZ6mrozJznA4b6azERwWwyTdIUUL00FXlw\nDMNhJwmIiAiT2uiIln9U/g==\n-----END PRIVATE KEY-----\n",
        "client_email": "hotel-787@hotel-mediafiles.iam.gserviceaccount.com",
        "client_id": "113622985753799247447",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/hotel-787%40hotel-mediafiles.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
)

GS_BUCKET_NAME = 'hotel_mediafiles'
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'https://storage.googleapis.com/{}/static/'.format(GS_BUCKET_NAME)
MEDIA_URL = 'https://storage.googleapis.com/{}/media/'.format(GS_BUCKET_NAME)


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'rooms.CustomUser'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://*.herokuapp.com",
    "https://*.gitpod.io",
    "https://*.codeinstitute-ide.net",
]

# Email configuration (update as needed)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Heroku settings
if 'DYNO' in os.environ:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
