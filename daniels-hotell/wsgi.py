"""
WSGI config for daniels-hotell project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from rooms.utils import log_storage_diagnostics
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daniels-hotell.settings")

application = get_wsgi_application()


log_storage_diagnostics()
