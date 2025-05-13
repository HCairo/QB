from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db.database import metadata, database

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=True),  # Nullable pour les comptes Google
    Column("name", String, nullable=True),
    Column("is_google_account", Boolean, default=False),
    Column("created_at", DateTime, server_default=func.now())
)

companies = Table(
    "companies", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("company_name", String, nullable=False),
    Column("siret", String, nullable=True),
    Column("sector", String, nullable=True),
    Column("address", String, nullable=True),
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

async def create_user_google(email: str, name: str):
    query = users.insert().values(email=email, name=name, is_google_account=True)
    user_id = await database.execute(query)
    return {"id": user_id, "email": email, "name": name}