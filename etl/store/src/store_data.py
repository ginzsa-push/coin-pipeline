import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import pyarrow.parquet as pq
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DBConnection(object):
    def __init__(self, host: str, port: int, user: str, password: str, db_name: str):
        self.db_host = host
        self.db_port = port
        self.db_user = user
        self.db_password = password
        self.db_name = db_name
        self.connection_string = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        self.db_engine = None

    def db_engine(self):
        """Create a SQLAlchemy engine for the database connection."""
        if not self.db_engine:
            self.db_engine = create_engine(self.connection_string)
        logger.info(f"Database engine created with connection string: {self.connection_string}")
        return self.db_engine


class ParquetToDB(object):
    def __init__(self, db_connection: DBConnection, table_name: str):
        self.db_connection = db_connection
        self.table_name = table_name

    def load_parquet(self, file_path: str) -> pd.DataFrame:
        """Load a Parquet file into a Pandas DataFrame."""
        return pq.read_table(file_path).to_pandas()

    def save_to_db(self, file_path: str) -> None:
        """Save the DataFrame to the database."""
        engine = self.db_connection.db_engine()
        df = pd.read_parquet(file_path)
        df.to_sql(self.table_name, con=engine, if_exists='replace', index=False, method='multi')

    def save_chunks_to_db(self, file_path: str, chunk_size: int = 10000) -> None:
        """Save the DataFrame to the database in chunks."""
        engine = self.db_connection.db_engine()
        parquet_file = pq.ParquetFile(file_path)
        total_rows = parquet_file.metadata.num_rows
        row_processed = 0
        first_chunk = True
        for batch in parquet_file.iter_batches(batch_size=chunk_size):
            df = batch.to_pandas()
            chunk_if_exists = 'replace' if first_chunk else 'append'
            df.to_sql(self.table_name, con=engine, if_exists=chunk_if_exists, index=False, method='multi')
            row_processed += len(df)
            first_chunk = False
            logger.info(f"Processed {row_processed}/{total_rows} rows.")    

        logger.info(f"All {total_rows} rows processed and saved to the database.")

def save_parquet_file_to_db(file_path: str):
    """Function to save a Parquet file to the database."""

    # get connection details from environment variables or config
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 5432))
    user = os.getenv('DB_USER', 'your_user')
    password = os.getenv('DB_PASSWORD', 'your_password')
    db_name = os.getenv('DB_NAME', 'your_db')

    db_connection = DBConnection(host, port, user, password, db_name)
    table_name = 'coin_fiat_data'
    
    parquet_to_db = ParquetToDB(db_connection, table_name)
    parquet_to_db.save_to_db(file_path)
    logger.info(f"Parquet file {file_path} saved to database table {table_name}.")

    