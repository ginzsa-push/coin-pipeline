# coin-pipeline

NOTE: This is a mock pipeline airflow project (Not to be used on production environment)

This uses CoinMarketCap API (Free access) for cripto tokens (coins)
https://coinmarketcap.com/api/documentation/v1/

And Exchange Rate for fiat 
https://api.exchangerate.host/live?access_key=myapikey

The ETL exersice will step through the followint

    1. extract data from boths apis
    2. transform aggregate and derive data into parquet file
    3. load parquet file into  a database


# Project structure



# Airflow
Follow instruction from Airflow docs [https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html]

# UV build

Using UV building project [https://docs.astral.sh/uv/guides/projects/#running-commands]

## UV project - install uv

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Database management

Uses alembic [https://alembic.sqlalchemy.org/en/latest/tutorial.html] 

Note: There are some 're arrengments' to do the first 'initial' run locally using UV
This will run Generate the first scheleton for alembic execution.
Note: for that it has the alembic.ini should be change to: localhost:5433
```
uv run alembic upgrade head
uv run alembic revision -m "create initial table creation"
```

# How to test

## integration test needs environment variables add exchange api token
```
export EXCHANGERATE_API_TOKEN=my-token 
export COINMARKETCAP_API_TOKEN=api_key_here
```

## UV build
```
uv build
```
NOTE dist folder will have the wheel artifact (to be deployed to an repository)
this should be used on the web api and airflow dags


## test locally (not working atm - conflict with airflow dbs)
```
docker compose build
docker compose up
```

Tear down local run (remove volume)
```
docker-compose down -v 
```

## Issues (so far)

UV and Airflow have known issues, spcially with the python 3.13 version

Running alembic db management could conflict with and airflow in a local environment
