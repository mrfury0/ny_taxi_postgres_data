
# NYC Taxi Postgres Data

This repository contains files and scripts for setting up a PostgreSQL database for ingesting NYC taxi data.

## File Structure

- `ingest_data.py`: Python script for ingesting NYC taxi data into the PostgreSQL database.
- `Dockerfile`: Dockerfile for creating a PostgreSQL container.
- `ny_taxi_postgres_data/`: Folder for storing PostgreSQL data.
- `output.csv`: Output CSV file.
- `output.csv.gz`: Compressed output CSV file.

## Docker Commands

### Start PostgreSQL Container

To start a PostgreSQL container for the NYC taxi database, run the following command:

```bash
docker run -d --name ny_taxi_postgres -p 5432:5432 --network=pg-network -v C:\\Users\\hanna\\Desktop\\data-engineering-zoomcamp\\2_docker_sql\\ny_taxi_postgres_data:/var/lib/postgresql/data ny_taxi_postgres
```

### Start pgAdmin Container

To start a pgAdmin container for database management, use the following command:

```bash
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin-2 \
dpage/pgadmin4
```

## Data Ingestion

To ingest NYC taxi data into the PostgreSQL database, run the following command:

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
python ingest_data.py \
--user=root \
--password=root \
--host=localhost \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_data \
--url=${URL}
```

This command will fetch the data from the specified URL and insert it into the `yellow_taxi_data` table in the `ny_taxi` database.

