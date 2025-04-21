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

    def __init__(self, *args, **kwargs):
        kwargs["default_acl"] = None
        super().__init__(*args, **kwargs)

    def url(self, name):
        """
        Gives correct MEDIA_URL and not google generated url.
        """
        try:
            return urljoin(settings.MEDIA_URL, name)
        except Exception as e:
            print(f"Error generating custom URL: {e}")
            return super().url(name)
