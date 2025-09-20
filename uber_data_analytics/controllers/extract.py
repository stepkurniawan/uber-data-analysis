import shutil

import kagglehub
import structlog

log = structlog.get_logger(__name__)


# Set the path to the file you'd like to load
def download_csv(dataset_identifier: str, file_path: str) -> None:
    # Load the latest version
    log.info("Starting data extraction", file_path=file_path)

    cache_path = kagglehub.dataset_download(dataset_identifier, path="ncr_ride_bookings.csv")

    # save it under file_path
    shutil.copy2(cache_path, file_path)

    log.info("Data extraction completed successfully")
