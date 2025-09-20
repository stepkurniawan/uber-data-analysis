from uber_data_analytics.controllers.load import StorageService
from uber_data_analytics.settings import Settings


class ResourceManager:
    def __init__(self):
        self.get_settings()
        self.get_storage_service()

    def get_settings(self):
        if not hasattr(self, "_settings"):
            self._settings = Settings()
        return self._settings

    def get_storage_service(self):
        if not hasattr(self, "_storage_service"):
            settings = self.get_settings()
            self._storage_service = StorageService(
                connection_settings=settings.s3_connection_settings
            )
        return self._storage_service


resource_manager = ResourceManager()
