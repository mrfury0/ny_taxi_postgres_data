import pandas as pd
from time import time
from sqlalchemy import create_engine
import os
import requests
import gzip  # Added import for gzip

import argparse

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    url=params.url
    table_name=params.table_name

    csv_name = 'output.csv.gz'  # Changed the file extension to .gz

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(csv_name, 'wb') as csv_file:
                csv_file.write(response.content)
            print("Download successful")
        else:
            print(f"Download failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Download failed: {str(e)}")

    # Define the database connection URL
    db_url = f'postgresql://{user}:{password}@{host}/{db}'

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    try:
        # Try to connect to the database by executing a simple query
        connection = engine.connect()
        print("Connected successfully")
        
        # Close the connection
        connection.close()
    except Exception as e:
        print(f"Connection failed: {str(e)}")

    # Decompress the downloaded .gz file
    with gzip.open(csv_name, 'rb') as compressed_file, open('output.csv', 'wb') as csv_file:
        csv_file.write(compressed_file.read())

    df_iter = pd.read_csv('output.csv', iterator=True, chunksize=100000)

    df= next(df_iter)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)

    df.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace')
    df.to_sql(name=table_name,con=engine,if_exists='append')

    while True:
        t_start=time()
        df = next(df_iter)
        df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
        df.to_sql(name=table_name,con=engine,if_exists='append')
        t_end=time()
        print(f"inserted another chunk..., took {t_end-t_start:.3f} seconds")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest csv data to postgres')

    # user,password,host,port,database,name,table,table name
    #url of csv 
    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--table_name',help='table-name for postgres')
    parser.add_argument('--url',help='url of csv files')

    args = parser.parse_args()
    main(args)
