import pandas as pd

jobs_df = pd.read_csv("data/indeed-job-listings.csv")
print(jobs_df.head())  # Print first 5 rows
print(jobs_df.columns)  # Print available column names
