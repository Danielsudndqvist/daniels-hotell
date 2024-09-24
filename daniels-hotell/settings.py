from pathlib import Path
import os
import environ
import dj_database_url
from django.conf import settings


env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent, '.env'))


BASE_DIR = Path(__file__).resolve().parent.parent

# Basic settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
DEBUG = True 
ALLOWED_HOSTS = ['8000-danielsudnd-danielshote-f9o9cx36nv8.ws.codeinstitute-ide.net']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rooms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

import dj_database_url

DATABASE_URL = "postgres://ufh1hsk3u2h:oWWzEgIQhjM1@ep-gentle-mountain-a23bxz6h-pooler.eu-central-1.aws.neon.tech/boned_come_essay_908735"

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net",
    "https://8000-danielsudndq-djangoblog-ukb6ligfpsq.ws.codeinstitute-ide.net"
]

# Password validation
AUTH_USER_MODEL = 'rooms.CustomUser'

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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

