from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("oracle+oracledb://system:oracle@localhost:1521/XE")


#Load data to dtb

calendar_df = pd.read_csv("transformed_data/calendar.csv")
calendar_df['start_time'] = pd.to_datetime(calendar_df['start_time'])
calendar_df['end_time']   = pd.to_datetime(calendar_df['end_time'])


df_events = (
        calendar_df[
            ['event_id', 'email','summary','description','start_time','end_time']
        ]
        )

df_events.to_sql(
  'stg_calendar_events',
  con=engine,
  if_exists='append',  # keep your table schema
  index=False
)
