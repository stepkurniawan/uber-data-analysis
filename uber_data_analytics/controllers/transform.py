import json

import pandas as pd
import structlog
from pydantic import ValidationError

from uber_data_analytics.controllers.bookings_schema import Booking

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
        df = pd.read_csv(file_path, sep=",", nrows=1000)  # Limit to first 1000 rows for performance

        # Clean column names by stripping whitespace
        df.columns = df.columns.str.strip()

        validated_bookings = []

        for _, row in df.iterrows():
            # Manually convert all NA/NaN values to None before Pydantic
            row_dict = {}
            for col, value in row.items():
                if pd.isna(value):  # This handles both np.nan and pd.NA
                    row_dict[col] = None
                else:
                    row_dict[col] = value

            booking = Booking.model_validate(row_dict, by_alias=True)
            validated_bookings.append(booking)

    except ValidationError as ve:
        log.error("Data validation error", error=str(ve))
        raise

    log.info(
        f"Data transformation and validation completed successfully. \
        Total records: {len(validated_bookings)}"
    )
    return validated_bookings


def create_json(bookings: list[Booking], output_path: str) -> str:
    """
    Create a JSON file from a list of Booking objects.

    Args:
        bookings (list[Booking]): List of Booking objects.
        output_path (str): Path to save the JSON file.
    """
    try:
        log.info("Starting JSON creation", output_path=output_path)
        booking_dicts = [booking.model_dump() for booking in bookings]

        with open(output_path, "w") as json_file:
            json.dump(booking_dicts, json_file, indent=4)

        log.info("JSON file created successfully", output_path=output_path)
        return output_path

    except Exception as e:
        log.error("Error creating JSON file", error=str(e))
        raise
