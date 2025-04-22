from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import metadata, database

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now())
)

invoices = Table(
    "invoices", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("client_name", String, nullable=False),
    Column("amount", Integer, nullable=False),
    Column("status", String, default="draft"),
    Column("created_at", DateTime, server_default=func.now())
)

async def get_user_by_email(email: str):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)