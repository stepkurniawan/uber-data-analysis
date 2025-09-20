import os
import structlog
import logging
from uber_data_analytics.resources import resource_manager
from uber_data_analytics.controllers.transform import transform_bookings
from uber_data_analytics.controllers.extract import download_csv

settings = resource_manager.get_settings()

log = structlog.get_logger(__name__)
logging.basicConfig(level=settings.log_level)


def main():
    log.info("Input file path", input_file_path=settings.input_file_path)

    if not os.path.exists(settings.input_file_path):
        log.info(f"Input file not found, downloading to {settings.input_file_path}")
        download_csv(settings.dataset_identifier, settings.input_file_path)
    else:
        log.info(f"Input file found at {settings.input_file_path}, skipping download")

    transform_bookings(settings.input_file_path)


if __name__ == "__main__":
    main()
