import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
from google.cloud import storage
import logging

class Command(BaseCommand):
    help = 'Comprehensive debugging script for static files collection and GCS upload'

    def handle(self, *args, **kwargs):
        logger = self.stdout.write

        # Debugging Static Root
        logger("### Static Files Debugging ###")
        logger(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        logger(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        logger(f"STATIC_URL: {settings.STATIC_URL}")

        # Check if static root exists
        if not os.path.exists(settings.STATIC_ROOT):
            self.stdout.write(self.style.WARNING(f"STATIC_ROOT directory does not exist: {settings.STATIC_ROOT}"))
            os.makedirs(settings.STATIC_ROOT, exist_ok=True)

        # Collect static files
        logger("Running collectstatic...")
        call_command('collectstatic', '--noinput', verbosity=2)

        # List collected static files
        logger("Collected Static Files:")
        for root, dirs, files in os.walk(settings.STATIC_ROOT):
            for file in files:
                filepath = os.path.join(root, file)
                self.stdout.write(filepath)

        # Google Cloud Storage Configuration
        logger("\n### Google Cloud Storage Configuration ###")
        logger(f"GS_BUCKET_NAME: {getattr(settings, 'GS_BUCKET_NAME', 'Not Set')}")
        logger(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        logger(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")

        # Manually upload to GCS
        try:
            # Check if GCS is configured
            if hasattr(settings, 'GS_BUCKET_NAME') and settings.GS_BUCKET_NAME:
                # Initialize GCS client
                client = storage.Client()
                bucket = client.get_bucket(settings.GS_BUCKET_NAME)

                # Upload static files
                for root, dirs, files in os.walk(settings.STATIC_ROOT):
                    for file in files:
                        local_path = os.path.join(root, file)
                        relative_path = os.path.relpath(local_path, settings.STATIC_ROOT)
                        gcs_path = f'static/{relative_path}'

                        # Upload blob
                        blob = bucket.blob(gcs_path)
                        blob.upload_from_filename(local_path)
                        self.stdout.write(f"Uploaded: {gcs_path}")

                # Verify GCS contents
                blobs = bucket.list_blobs(prefix='static/')
                logger("\n### GCS Static Files ###")
                for blob in blobs:
                    self.stdout.write(f"GCS File: {blob.name}")
            else:
                self.stdout.write(self.style.WARNING("GCS Bucket not configured"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"GCS Upload Error: {e}"))
