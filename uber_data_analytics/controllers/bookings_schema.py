import pandas as pd
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    computed_field,
    field_serializer,
)
from datetime import datetime


class Booking(BaseModel):
    date: str = Field(
        ..., description="Date of the booking in YYYY-MM-DD format", alias="Date"
    )
    time: str = Field(
        ..., description="Time of the booking in HH:MM:SS format", alias="Time"
    )
    booking_id: str = Field(
        ...,
        description="Unique identifier for the booking",
        examples=["BKG12345"],
        alias="Booking ID",
    )
    booking_status: str = Field(
        ...,
        description="Status of the booking",
        examples=["completed", "cancelled", "incomplete"],
        alias="Booking Status",
    )
    customer_id: str = Field(
        ...,
        description="Unique identifier for the customer",
        examples=["CUST67890"],
        alias="Customer ID",
    )
    vehicle_type: str = Field(
        ...,
        description="Type of vehicle booked",
        examples=["sedan", "suv", "hatchback"],
        alias="Vehicle Type",
    )
    pickup_location: str = Field(
        ...,
        description="Location where the ride starts",
        examples=["Downtown", "Airport"],
        alias="Pickup Location",
    )
    drop_location: str = Field(
        ...,
        description="Location where the ride ends",
        examples=["Mall", "Hotel"],
        alias="Drop Location",
    )
    avg_vtat: float | None = Field(
        ...,
        description="Average Vehicle Time to Arrival in minutes",
        examples=[5.0],
        alias="Avg VTAT",
    )
    avg_ctat: float | None = Field(
        ...,
        description="Average Customer Time to Arrival in minutes",
        examples=[3.0],
        alias="Avg CTAT",
    )
    cancelled_rides_by_customer: bool | None = Field(
        ...,
        description="Customer-initiated cancellation flag",
        examples=[1],
        alias="Cancelled Rides by Customer",
    )
    reason_for_cancelling_by_customer: str | None = Field(
        ...,
        description="Reason for cancellation by the customer",
        examples=["Changed mind", "Found alternative"],
        alias="Reason for cancelling by Customer",
    )
    cancelled_rides_by_driver: bool | None = Field(
        ...,
        description="Driver-initiated cancellation flag",
        examples=[1],
        alias="Cancelled Rides by Driver",
    )
    driver_cancellation_reason: str | None = Field(
        ...,
        description="Reason for cancellation by the driver",
        examples=["Traffic", "Vehicle issue"],
        alias="Driver Cancellation Reason",
    )
    incomplete_rides: bool | None = Field(
        ..., description="Incomplete ride flag", examples=[1], alias="Incomplete Rides"
    )
    incomplete_rides_reason: str | None = Field(
        ...,
        description="Reason for incomplete rides",
        examples=["Customer no-show", "Driver no-show"],
        alias="Incomplete Rides Reason",
    )
    booking_value: float | None = Field(
        ...,
        description="Monetary value of the booking",
        examples=[25.50],
        alias="Booking Value",
    )
    ride_distance: float | None = Field(
        ...,
        description="Distance of the ride in kilometers",
        examples=[12.5],
        alias="Ride Distance",
    )
    driver_ratings: float | None = Field(
        ...,
        description="Rating given by the driver",
        examples=[4.5],
        alias="Driver Ratings",
    )
    customer_rating: float | None = Field(
        ...,
        description="Rating given by the customer",
        examples=[4.7],
        alias="Customer Rating",
    )
    payment_method: str | None = Field(
        ...,
        description="Method of payment used",
        examples=["credit_card", "cash", "wallet"],
        alias="Payment Method",
    )

    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "cancelled_rides_by_customer",
        "cancelled_rides_by_driver",
        "incomplete_rides",
        mode="before",
    )
    @classmethod
    def validate_boolean_flags(cls, v):
        """Convert integer flags to boolean."""
        if v is None:
            return False
        if v == 1:
            return True
        elif v == 0:
            return False
        raise ValueError("Flag must be 0, 1, or None")

    @field_validator(
        "reason_for_cancelling_by_customer",
        "driver_cancellation_reason",
        "incomplete_rides_reason",
        "payment_method",
        mode="before",
    )
    @classmethod
    def validate_optional_strings(cls, v):
        """Convert NaN to None for optional string fields."""
        if pd.isna(v):
            return None
        return v

    @computed_field
    @property
    def datetime(self) -> datetime:
        """Combine date and time into a single datetime object."""
        return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M:%S")

    @computed_field
    @property
    def total_wait_time(self) -> float | None:
        """Calculate total wait time (VTAT + CTAT)."""
        if self.avg_vtat is not None and self.avg_ctat is not None:
            return self.avg_vtat + self.avg_ctat
        return None

    @field_serializer("datetime")
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return dt.isoformat()
