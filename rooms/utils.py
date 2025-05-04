import logging
import os
from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger("storage_diagnostics")


def log_storage_diagnostics():
    """Log detailed diagnostics about storage and environment"""
    logger.debug("Starting Storage Diagnostics")

    # Google Cloud Storage settings
    logger.debug(f"Is Development: {settings.IS_DEVELOPMENT}")
    logger.debug(f"Bucket Name: {settings.GS_BUCKET_NAME}")

    # Storage backend
    logger.debug(f"Default Storage: {default_storage.__class__.__name__}")

    # Environment variables
    env_vars = ["DJANGO_ENV", "GS_BUCKET_NAME", "GS_PROJECT_ID", "DEBUG"]

    for var in env_vars:
        value = os.environ.get(var, "NOT SET")
        logger.debug(f"{var}: {value}")

    # Credentials check
    try:
        credentials = getattr(settings, "GS_CREDENTIALS", None)
        if credentials:
            logger.debug("Google Cloud Credentials: Loaded successfully")
        else:
            logger.warning("No Google Cloud Credentials found")
    except Exception as e:
        logger.error(f"Credentials Check Error: {e}")
