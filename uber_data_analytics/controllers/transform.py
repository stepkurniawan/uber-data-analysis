import pandas as pd
from pydantic import ValidationError
import structlog

from uber_data_analytics.schemas.transform import Booking

log = structlog.get_logger(__name__)


def transform_bookings(file_path: str) -> list[Booking]:
    """
    Extract booking data from a CSV file and return as a list of Booking objects.

    Args:
        file_path (str): Path to the CSV file containing booking data.

    Returns:
        list[Booking]: List of Booking objects.
    """
    try:
        log.info("Starting transformation from CSV", file_path=file_path)
        df = pd.read_csv(
            file_path, nrows=10000, sep=","
        )  # Limiting to first 100 rows for performance

        validated_bookings = []

        for _, row in df.iterrows():
            # Manually convert all NA/NaN values to None before Pydantic
            row_dict = {}
            for col, value in row.items():
                if pd.isna(value):  # This handles both np.nan and pd.NA
                    row_dict[col] = None
                else:
                    row_dict[col] = value

            booking = Booking(**row_dict)
            validated_bookings.append(booking.model_dump())

    except ValidationError as ve:
        log.error("Data validation error", error=str(ve))
        raise

    log.info("Data transformation and validation completed successfully")
    return validated_bookings
