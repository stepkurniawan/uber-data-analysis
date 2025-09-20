# uber-data-analysis
Data ETL from this kaggle : https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard?resource=download&amp;select=ncr_ride_bookings.csv

Pipeline:
1. Download the dataset from kaggle using kaggle API (you need to have kaggle API token in ~/.kaggle/kaggle.json)
2. Abusing pandas and pydantic to transform and validate the data
3. Load the data into an S3 bucket (localstack for now)
