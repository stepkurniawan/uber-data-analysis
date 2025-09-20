from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = Field("MyApp", env="APP_NAME")
    input_file_path: str = Field("uber_data_analytics/data/input.csv", env="INPUT_FILE_PATH")
    output_file_path: str = Field(
        "uber_data_analytics/data/processed_bookings.json", env="OUTPUT_FILE_PATH"
    )
    log_level: str = Field("INFO", env="LOG_LEVEL")
    dataset_identifier: str = "yashdevladdha/uber-ride-analytics-dashboard"

    # s3 settings
    s3_endpoint_url: str | None = None
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_bucket_name: str | None = "my-bucket"
    s3_region_name: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def s3_connection_settings(self) -> dict[str, Any]:
        """Return S3 connection settings as a dictionary."""
        if self.s3_endpoint_url and self.s3_access_key_id and self.s3_secret_access_key:
            return {
                "service_name": "s3",
                "endpoint_url": self.s3_endpoint_url,
                "aws_access_key_id": self.s3_access_key_id,
                "aws_secret_access_key": self.s3_secret_access_key,
                "region_name": self.s3_region_name,
            }
        return {"service_name": "s3", "region_name": self.s3_region_name}
