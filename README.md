# Uber Data Analytics ETL Pipeline

A robust ETL (Extract, Transform, Load) pipeline for processing Uber ride booking data from Kaggle, featuring data validation with Pydantic and cloud storage integration.

## 📊 Project Overview

This project implements a complete data pipeline that:
- Extracts Uber ride booking data from Kaggle
- Transforms and validates data using Pydantic models
- Loads processed data to S3-compatible storage (LocalStack for development)

**Data Source**: [Uber Ride Analytics Dashboard](https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard)

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Kaggle    │───▶│   Transform  │───▶│   S3 Bucket │
│  (Extract)  │    │  & Validate  │    │   (Load)    │
└─────────────┘    └──────────────┘    └─────────────┘
```

### Pipeline Components

1. **Extract** ([`controllers/extract.py`](uber_data_analytics/controllers/extract.py))
   - Downloads NCR ride bookings CSV from Kaggle using `kagglehub`
   - Handles dataset caching and file management

2. **Transform** ([`controllers/transform.py`](uber_data_analytics/controllers/transform.py))
   - Processes CSV data with pandas
   - Validates booking records using Pydantic models
   - Converts data to JSON format

3. **Load** ([`services/storage_service.py`](uber_data_analytics/services/storage_service.py))
   - Uploads processed data to S3-compatible storage
   - Supports both AWS S3 and LocalStack

## 📋 Data Schema

The pipeline processes booking data with the following structure (defined in [`controllers/bookings_schema.py`](uber_data_analytics/controllers/bookings_schema.py)):

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Booking date (YYYY-MM-DD) |
| `time` | string | Booking time (HH:MM:SS) |
| `booking_id` | string | Unique booking identifier |
| `booking_status` | string | Status (completed/cancelled/incomplete) |
| `customer_id` | string | Customer identifier |
| `vehicle_type` | string | Vehicle type (sedan/suv/hatchback) |
| `pickup_location` | string | Pickup location |
| `drop_location` | string | Drop-off location |
| `avg_vtat` | float | Average Vehicle Time to Arrival (minutes) |
| `avg_ctat` | float | Average Customer Time to Arrival (minutes) |
| `booking_value` | float | Monetary value of booking |
| `ride_distance` | float | Distance in kilometers |
| `driver_ratings` | float | Driver rating |
| `customer_rating` | float | Customer rating |
| `payment_method` | string | Payment method used |

### Computed Fields
- `datetime`: Combined date/time as ISO datetime
- `total_wait_time`: Sum of VTAT and CTAT

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Kaggle API credentials
- Docker (for LocalStack)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd uber-data-analysis
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   ```

3. **Set up Kaggle API**
   ```bash
   # Create kaggle directory
   mkdir ~/.kaggle

   # Add your kaggle.json credentials file
   cp kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```


### Local Development with LocalStack

1. **Start LocalStack**
   ```bash
   sudo localstack start
   ```

2. **Create S3 bucket**
   ```bash
   awslocal s3 mb s3://my-bucket
   ```

## 🏃‍♂️ Usage

### Run the Complete Pipeline

```bash
# Using uv
uv run python -m uber_data_analytics.main

# Or directly
python -m uber_data_analytics.main
```

## 📁 Project Structure

```
uber-data-analysis/
├── uber_data_analytics/
│   ├── controllers/           # Data processing logic
│   │   ├── extract.py        # Kaggle data extraction
│   │   ├── transform.py      # Data transformation
│   │   └── bookings_schema.py # Pydantic data models
│   ├── services/             # External service integrations
│   │   └── storage_service.py # S3 storage operations
│   ├── data/                 # Data files (gitignored)
│   ├── main.py              # Main pipeline orchestrator
│   ├── settings.py          # Configuration management
│   └── resources.py         # Dependency injection
├── tests/                   # Test suite
├── notebooks/              # Jupyter notebooks for exploration
├── .github/workflows/      # CI/CD pipelines
└── pyproject.toml         # Project configuration
```
