from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = Field("MyApp", env="APP_NAME")
    input_file_path: str = Field(
        "uber_data_analytics/data/input.csv", env="INPUT_FILE_PATH"
    )
    log_level: str = Field("INFO", env="LOG_LEVEL")
    dataset_identifier: str = "yashdevladdha/uber-ride-analytics-dashboard"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
