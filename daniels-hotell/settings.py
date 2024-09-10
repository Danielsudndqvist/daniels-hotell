from pathlib import Path
import os
import environ
import dj_database_url
from django.conf import settings

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Basic settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')  # Use a default for local development
DEBUG = True  # Set to False in production
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

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://ufh1hsk3u2h:oWWzEgIQhjM1@ep-gentle-mountain-a23bxz6h-pooler.eu-central-1.aws.neon.tech/boned_come_essay_908735'
    )
}


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Directory where static files will be collected when running collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Directories where Django will search for static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

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

# Jazzmin settings
JAZZMIN_SETTINGS = {
    'site_header': "Hotel",
    'site_brand': "",
    'site_logo': "",
    'copyright': "All Rights Reserved 2024",
    "welcome_sign": "",
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Company", "url": "/admin/addons/company/"},
        {"name": "Users", "url": "/admin/userauths/user/"},
        {"model": "auth.user"},
    ],
    "order_with_respect_to": [
        "hotel",
        "hotel.Hotel",
        "hotel.Room",
        "hotel.Booking",
        "hotel.BookingDetail",
        "hotel.Guest",
        "hotel.RoomServices",
        "userauths",
        "addons",
    ],
    "icons": {
        "admin.LogEntry": "fas fa-file",
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "userauths.User": "fas fa-user",
        "userauths.Profile": "fas fa-address-card",
        "hotel.Hotel": "fas fa-th",
        "hotel.Booking": "fas fa-calendar-week",
        "hotel.BookingDetail": "fas fa-calendar-alt",
        "hotel.Guest": "fas fa-user",
        "hotel.Room": "fas fa-bed",
        "hotel.RoomServices": "fas fa-user-cog",
        "hotel.Notification": "fas fa-bell",
        "hotel.Coupon": "fas fa-tag",
        "hotel.Bookmark": "fas fa-heart",
    },
    "show_ui_builder": True
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-olive",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
