from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json

class Command(BaseCommand):
    help = 'Detailed static files configuration diagnostic'

    def handle(self, *args, **kwargs):
        # Print out detailed static files configuration
        self.stdout.write(self.style.SUCCESS("=== Static Files Configuration ==="))
        
        # Basic configuration
        self.stdout.write(f"STATIC_URL: {settings.STATIC_URL}")
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Check if directories exist
        self.stdout.write("\n=== Directory Existence ===")
        self.stdout.write(f"STATIC_ROOT exists: {os.path.exists(settings.STATIC_ROOT)}")
        
        for directory in settings.STATICFILES_DIRS:
            self.stdout.write(f"Static directory {directory} exists: {os.path.exists(directory)}")
        
        # List files in static directories
        self.stdout.write("\n=== Static Files Inventory ===")
        for directory in settings.STATICFILES_DIRS:
            self.stdout.write(f"\nFiles in {directory}:")
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        filepath = os.path.join(root, file)
                        relative_path = os.path.relpath(filepath, directory)
                        self.stdout.write(f"  {relative_path}")
        
        # Check STATIC_ROOT files
        self.stdout.write("\n=== Collected Static Files ===")
        if os.path.exists(settings.STATIC_ROOT):
            for root, dirs, files in os.walk(settings.STATIC_ROOT):
                for file in files:
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, settings.STATIC_ROOT)
                    self.stdout.write(f"  {relative_path}")
        
        # Storage backend information
        self.stdout.write("\n=== Storage Configuration ===")
        try:
            from django.contrib.staticfiles.storage import staticfiles_storage
            self.stdout.write(f"Storage Backend: {staticfiles_storage.__class__.__name__}")
            self.stdout.write(f"Base URL: {staticfiles_storage.base_url}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error retrieving storage info: {e}"))
