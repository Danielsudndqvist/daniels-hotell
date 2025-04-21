"""
ASGI config for daniels-hotell project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from rooms.utils import log_storage_diagnostics
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daniels-hotell.settings")

application = get_asgi_application()
log_storage_diagnostics()
