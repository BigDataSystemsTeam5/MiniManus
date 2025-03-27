import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from snowflake.snowpark import Session

load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')


connection_params = {
    "account": os.getenv('SNOWFLAKE_ACCOUNT'),
    "user": os.getenv('SNOWFLAKE_USER'),
    "password": os.getenv('SNOWFLAKE_PASSWORD'),
    "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
    "database": os.getenv('SNOWFLAKE_DATABASE'),
    "schema": os.getenv('SNOWFLAKE_SCHEMA')
}


@tool("snowflake_data")
def snowflake_data(year: int, quarter: int):
    """Finds information from snowflake database using a SQL query
    and a specific year and quarter. Allows us to learn more details about a specific report."""

    # Create Snowflake session
    session = Session.builder.configs(connection_params).create()

    if quarter == 1:
        mon = 'April'
    elif quarter == 2:
        mon = 'July'
    elif quarter == 3:
        mon = 'Oct'
    elif quarter == 4:
        mon = 'Jan'
    
    if quarter == 4:
        year = year+1
    
    year = str(year)
    column = f"{mon}_{year}"

    # Execute a SQL query
    df = session.sql(f'SELECT "Measures", "Current", "{column}" FROM NVIDIA_KEY_STATS')

    # Collect results as a list
    result = df.collect()

    return result