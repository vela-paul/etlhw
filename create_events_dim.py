from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("oracle+oracledb://system:oracle@localhost:1521/XE")


#Load data to dtb

calendar_df = pd.read_csv("transformed_data/calendar.csv")
meetings_df = pd.read_csv("transformed_data/meetings.csv")
participants_df = pd.read_csv("transformed_data/participants.csv")


print(calendar_df.head())



# 3. Write into Oracle (after making event_id an IDENTITY on the table)
calendar_df.to_sql(
  'dim_events',
  con=engine,
  if_exists='append',  # keep your table schema
  index=False
)
#calendar_df.to_sql('dim_events', con=engine, if_exists='replace', index=False)