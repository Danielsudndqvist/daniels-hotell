from storages.backends.gcloud import GoogleCloudStorage

class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """Google Cloud Storage class for media files."""
    
    def __init__(self, *args, **kwargs):
        kwargs.update({"location": "media"})
        # No predefinedAcl parameter for uniform bucket-level access
        super().__init__(*args, **kwargs)

class GoogleCloudStaticFileStorage(GoogleCloudStorage):
    """Google Cloud Storage class for static files."""
    
    def __init__(self, *args, **kwargs):
        kwargs.update({"location": "static"})
        # No predefinedAcl parameter for uniform bucket-level access
        super().__init__(*args, **kwargs)
