from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
from google.cloud import storage

class Command(BaseCommand):
    help = 'Upload static files to Google Cloud Storage'

    def handle(self, *args, **kwargs):
        # Print out environment and settings for debugging
        self.stdout.write("Debugging GCS Upload")
        self.stdout.write(f"DJANGO_ENV: {os.environ.get('DJANGO_ENV')}")
        self.stdout.write(f"GS_BUCKET_NAME from settings: {getattr(settings, 'GS_BUCKET_NAME', 'Not Set')}")
        
        # Check for Google Cloud credentials
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        credentials_json = os.environ.get('GOOGLE_CREDENTIALS')
        
        if credentials_path:
            self.stdout.write(f"Credentials path: {credentials_path}")
        elif credentials_json:
            self.stdout.write("Credentials found in environment variable")
        else:
            self.stdout.write(self.style.ERROR("No Google Cloud credentials found"))
            return

        # Manually set bucket name
        bucket_name = 'hotel_media_bucket'  # Replace with your actual bucket name

        try:
            # Initialize GCS client
            client = storage.Client()
            bucket = client.get_bucket(bucket_name)

            # Walk through staticfiles directory
            static_root = settings.STATIC_ROOT
            self.stdout.write(f"Static Root: {static_root}")

            for root, dirs, files in os.walk(static_root):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, static_root)
                    blob_name = f'static/{relative_path}'

                    # Upload blob
                    blob = bucket.blob(blob_name)
                    blob.upload_from_filename(local_path)
                    self.stdout.write(f'Uploaded: {blob_name}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error uploading to GCS: {e}"))
