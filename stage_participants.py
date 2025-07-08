import pandas as pd
from sqlalchemy import create_engine, types

# 1. Read the participants CSV and parse dates
df = pd.read_csv("transformed_data/participants.csv", parse_dates=["First Join", "Last Leave"])

# 2. Normalize column names and select only the staging columns
df = df.rename(columns={
    "Name":                 "name",
    "First Join":           "first_join",
    "Last Leave":           "last_leave",
    "In-Meeting Duration":  "in_meeting_duration",
    "Email":                "email",
    "Participant ID (UPN)": "participant_id",
    "Role":                 "role",
    "meeting_id":           "meeting_id"
})[
    ["name", "first_join", "last_leave", "in_meeting_duration",
     "email",  "role", "meeting_id"]
]

# 3. Ensure datetimes are real Python datetime objects
df["first_join"] = pd.to_datetime(df["first_join"])
df["last_leave"] = pd.to_datetime(df["last_leave"])

# 4. Cast duration to numeric (seconds)
df["in_meeting_duration"] = pd.to_numeric(df["in_meeting_duration"], errors="coerce")

#
engine = create_engine("oracle+oracledb://system:oracle@localhost:1521/XE")


df.to_sql(
    "stg_participants",
    con=engine,
    if_exists="append",
    index=False,
  
)

