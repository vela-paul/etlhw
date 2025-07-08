import pandas as pd
from sqlalchemy import create_engine, types

# 1. Read the CSV, strip stray quotes, and parse dates
df = pd.read_csv("transformed_data/meetings.csv")
df["start_time"] = pd.to_datetime(
    df["start_time"].str.replace('"', ""),
    format="%m/%d/%y, %I:%M:%S %p"
)
df["end_time"] = pd.to_datetime(
    df["end_time"].str.replace('"', ""),
    format="%m/%d/%y, %I:%M:%S %p"
)

# 2. Select & rename to match DIM_MEETINGS
load_df = df.rename(columns={"meeting_title": "title"})[
    ["title", "start_time", "end_time"]
]

# 3. Create the engine (update with your credentials)

engine = create_engine("oracle+oracledb://system:oracle@localhost:1521/XE")

# 4. Append to DIM_MEETINGS
load_df.to_sql(
    "dim_meetings",
    con=engine,
    if_exists="append",
    index=False,
    dtype={
        "start_time": types.Date(),
        "end_time":   types.Date()
    }
)

print("DIM_MEETINGS populated successfully.")
