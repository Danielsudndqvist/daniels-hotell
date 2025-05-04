from urllib.parse import urljoin
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """
    Google file storage class which gives a media
    file path from MEDIA_URL not google generated one.
    """

    bucket_name = setting("GS_BUCKET_NAME")
    location = 'media'  # Add this line to set the subdirectory

    def __init__(self, *args, **kwargs):
        kwargs["default_acl"] = "publicRead"  # Change to publicRead
        super().__init__(*args, **kwargs)

    def url(self, name):
        """
        Returns the full GCS URL for accessing the file.
        """
        # Let the GoogleCloudStorage parent class handle the URL generation
        return super().url(name)
