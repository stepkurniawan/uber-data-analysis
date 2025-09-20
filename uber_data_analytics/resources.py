from uber_data_analytics.settings import Settings


class ResourceManager:
    def __init__(self):
        self.get_settings()

    def get_settings(self):
        if not hasattr(self, "_settings"):
            self._settings = Settings()
        return self._settings


resource_manager = ResourceManager()
