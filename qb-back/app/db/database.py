import os
from databases import Database
from sqlalchemy import create_engine, MetaData

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))