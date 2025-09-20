from pathlib import Path
from typing import Any
import structlog
import boto3

log = structlog.get_logger(__name__)


class StorageService:
    def __init__(self, connection_settings: dict[str, Any]):
        self.connection_settings = connection_settings

    def get_client(self):
        if not hasattr(self, "_client"):
            self._client = boto3.client(**self.connection_settings)
        return self._client

    def list_files(self, bucket_name: str, prefix: str = "") -> list[str]:
        try:
            log.info(f"Listing files in bucket: {bucket_name} with prefix: {prefix}")
            s3_client = self.get_client()
            objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            files = [obj["Key"] for obj in objects.get("Contents", [])]
            log.info(f"Found {len(files)} files")
            return files
        except Exception as e:
            log.error(f"Error listing files: {e}")
            return []

    def upload_file(self, file_path: Path, remote_path: str, bucket_name: str) -> None:
        try:
            log.info(
                f"Uploading {file_path}", bucket=bucket_name, local_file_path=file_path
            )
            s3_client = self.get_client()
            target_path = f"{remote_path}/{file_path.name}"
            s3_client.upload_file(
                Filename=str(file_path), Bucket=bucket_name, Key=target_path
            )
            log.info(f"File uploaded successfully to {target_path}")

        except Exception as e:
            log.error(f"Error uploading file: {e}")

    def download_file(
        self, remote_path: str, local_file_path: Path, bucket_name: str
    ) -> None:
        try:
            log.info(
                f"Downloading {remote_path}",
                bucket=bucket_name,
                local_file_path=local_file_path,
            )
            s3_client = self.get_client()
            s3_client.download_file(
                Bucket=bucket_name, Key=remote_path, Filename=str(local_file_path)
            )
            log.info(f"File downloaded successfully to {local_file_path}")

        except Exception as e:
            log.error(f"Error downloading file: {e}")

    def delete_file(self, remote_path: str, bucket_name: str) -> None:
        try:
            log.info(f"Deleting {remote_path}", bucket=bucket_name)
            s3_client = self.get_client()
            s3_client.delete_object(Bucket=bucket_name, Key=remote_path)
            log.info(f"File deleted successfully from {remote_path}")

        except Exception as e:
            log.error(f"Error deleting file: {e}")
