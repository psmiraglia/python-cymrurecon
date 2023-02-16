# Ingest records into InfluxDB

1.  Install dependencies

        pip install -r requirements.txt

2.  Run local InfluxDB into a Docker container (opional)

        ./run-influxdb.sh

3.  Run the ingestor

        RECON_QUERY_ID=... RECON_API_KEY=... ./ingest_to_influxdb.py

    If you want to ingest an existing InfluxDB instance you can set the evironment variables
    
    * `INFLUXDB_URL`
    * `INFLUXDB_TOKEN`
    * `INFLUXDB_ORG`
    * `INFLUXDB_BUCKET`
