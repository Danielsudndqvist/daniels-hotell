from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin
from django.conf import settings


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """Simple Google Cloud Storage media file storage."""

    bucket_name = setting("GS_BUCKET_NAME")

    def __init__(self, *args, **kwargs):
        kwargs["default_acl"] = None
        super().__init__(*args, **kwargs)

    def url(self, name):
        """Generate URL for the file."""
        try:
            return urljoin(settings.MEDIA_URL, name)
        except Exception as e:
            print(f"URL generation error: {e}")
            return super().url(name)
