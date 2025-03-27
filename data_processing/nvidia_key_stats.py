import os
from dotenv import load_dotenv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from snowflake.snowpark import Session

# URL of the webpage to scrape
url = "https://finance.yahoo.com/quote/NVDA/key-statistics/"

# Send a GET request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)

data = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extract all table rows
    tables = soup.find_all('table')
    #for table in tables:
    rows = tables[0].find_all('tr')
    for row in rows:
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Set the first row as column names
    df.columns = df.iloc[0]  # Set first row as header
    df = df[1:]  # Drop the first row

    # Set the first column as the index
    df = df.set_index(df.columns[0])

    # Convert index into a column before storing in Snowflake (since SQL tables don't support index)
    df.reset_index(inplace=True)

    df.columns = ['Measures', 'Current', 'Jan_2025', 'Oct_2024', 'July_2024', 'April_2024', 'Jan_2024']
    #print(df)

else:
    print("Failed to retrieve page")


load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')


connection_params = {
    "account": os.getenv('SNOWFLAKE_ACCOUNT'),
    "user": os.getenv('SNOWFLAKE_USER'),
    "password": os.getenv('SNOWFLAKE_PASSWORD'),
    "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
    "database": os.getenv('SNOWFLAKE_DATABASE'),
    "schema": os.getenv('SNOWFLAKE_SCHEMA')
}

# Create Snowflake session
session = Session.builder.configs(connection_params).create()

# Ensure schema exists
session.sql(f"CREATE SCHEMA IF NOT EXISTS {connection_params['schema']}").collect()
print(f"Schema '{connection_params['schema']}' is ready.")


# Convert Pandas DataFrame to Snowpark DataFrame
snowflake_df = session.create_dataframe(df)

# Define table name
TABLE_NAME = "NVIDIA_KEY_STATS"
table = session.table(TABLE_NAME)

# Step 3: Drop the table
table.drop_table()

# Write DataFrame to Snowflake
snowflake_df.write.mode("overwrite").save_as_table(TABLE_NAME)

print(f"Data successfully uploaded to table '{TABLE_NAME}' in Snowflake!")