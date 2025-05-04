from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """Google Cloud Storage class for media files."""
    
    bucket_name = setting("GS_BUCKET_NAME")
    location = 'media'  # Store files in a 'media' subdirectory
    
    def __init__(self, *args, **kwargs):
        kwargs["default_acl"] = "publicRead"  # Make files publicly accessible
        super().__init__(*args, **kwargs)
    
    def url(self, name):
        """Return the URL for accessing the file."""
        return super().url(name)
