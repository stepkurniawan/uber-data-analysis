import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from uber_data_analytics.controllers.transform import transform_bookings
import os

TEMP_CSV_PATH = "tests/data/temp_test_input.csv"
@pytest.fixture
def example_input_data():
    df = pd.read_csv("tests/data/test_input.csv", nrows=10)
    return df

def test_transform_bookings(example_input_data):
    # Save the example input data to a temporary CSV file
    example_input_data.to_csv(TEMP_CSV_PATH, index=False)

    bookings = transform_bookings(TEMP_CSV_PATH)
    assert len(bookings) == 4  # Assuming all rows are valid


    # Clean up the temporary file

    os.remove(TEMP_CSV_PATH)


def test_create_json(example_input_data):
    # Save the example input data to a temporary CSV file
    example_input_data.to_csv(TEMP_CSV_PATH, index=False)

    bookings = transform_bookings(TEMP_CSV_PATH)
    output_path = "tests/data/temp_output.json"

    from uber_data_analytics.controllers.transform import create_json

    json_path = create_json(bookings, output_path=output_path)
    assert os.path.exists(json_path)

    with open(json_path, "r") as f:
        data = f.read()
        assert len(data) > 0

    # Clean up the temporary files
    os.remove(TEMP_CSV_PATH)
    os.remove(output_path)