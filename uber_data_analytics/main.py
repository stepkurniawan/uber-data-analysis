import os
from pathlib import Path
import structlog
import logging
from uber_data_analytics.resources import resource_manager
from uber_data_analytics.controllers.transform import transform_bookings, create_json
from uber_data_analytics.controllers.extract import download_csv

settings = resource_manager.get_settings()

log = structlog.get_logger(__name__)
logging.basicConfig(level=settings.log_level)


def main():
    storage_service = resource_manager.get_storage_service()
    log.info("Input file path", input_file_path=settings.input_file_path)

    if not os.path.exists(settings.input_file_path):
        log.info(f"Input file not found, downloading to {settings.input_file_path}")
        download_csv(settings.dataset_identifier, settings.input_file_path)
    else:
        log.info(f"Input file found at {settings.input_file_path}, skipping download")

    bookings = transform_bookings(settings.input_file_path)

    create_json(
        bookings,
        output_path=settings.output_file_path,
    )

    storage_service.upload_file(
        file_path=Path(settings.output_file_path),
        remote_path="",
        bucket_name=settings.s3_bucket_name,
    )

    files = storage_service.list_files(bucket_name=settings.s3_bucket_name)
    log.info(f"Files in bucket {settings.s3_bucket_name}: {files}")
    log.info("Process completed successfully")


if __name__ == "__main__":
    main()
