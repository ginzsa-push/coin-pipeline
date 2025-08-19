import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

# Load DATABASE_URL from environment (injected via docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/")
def ping():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW() as current_time"))
        row = result.fetchone()
        return {"db_time": str(row["current_time"])}

@app.get("/coinsfiat")    
def ping():
    with engine.connect() as conn:
        # TODO - pagination is required here
        result = conn.execute(text("SELECT * from coin_fiat_table LIMIT 1000"))
        rows = result.fetchall()
        return {"records": [dict(row) for row in rows]}