# ping dags to check if the ETL pipeline is running correctly

import logging
from airflow import DAG
from airflow.operators.empty import EmptyOperator


from datetime import datetime, timedelta   

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

def ping_etl():
    logger.info("ETL pipeline is running correctly.")
    operator = EmptyOperator(task_id='ping_etl_task')
    return operator