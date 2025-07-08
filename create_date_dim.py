
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, MetaData, Table

# 1. Set up date range: past 2 months from today
end_date = date.today()
start_date = end_date - relativedelta(months=2)

# 2. Generate a date sequence
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# 3. Build DataFrame for the Date Dimension
df = pd.DataFrame({
    'date_key': dates.strftime('%Y%m%d').astype(int),  # YYYYMMDD as integer PK
    'full_date': dates.date,                            # actual date
    'day_of_week': dates.day_name(),                    # Monday, Tuesday, …
    'month': dates.month,                               # 1–12
    'year': dates.year                                  # 2025, etc.
})

# 4. Define the table schema (Oracle example)

engine = create_engine("oracle+oracledb://system:oracle@localhost:1521/XE")
metadata = MetaData()

dim_date = Table(
    'dim_date', metadata,
    Column('date_key', Integer, primary_key=True),
    Column('full_date', Date, nullable=False),
    Column('day_of_week', String(9), nullable=False),
    Column('month', Integer, nullable=False),
    Column('year', Integer, nullable=False),
)

# 5. Create the table in the database (if it doesn't already exist)
metadata.create_all(engine)

# 6. Load the data into the table
df.to_sql('dim_date', con=engine, if_exists='append', index=False)

# 7. (Optional) Preview the first few rows
print(df.head())
