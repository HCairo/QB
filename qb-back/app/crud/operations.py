from app.security.password import hash_password
from app.db.database import database
from app.db.models import users, invoices

async def create_user(user_data):
    hashed_password = hash_password(user_data.password)
    query = users.insert().values(
        email=user_data.email,
        hashed_password=hashed_password
    )
    user_id = await database.execute(query)
    user_query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(user_query)

async def create_invoice(user_id: int, invoice_data):
    query = invoices.insert().values(
        user_id=user_id,
        client_name=invoice_data.client_name,
        amount=invoice_data.amount,
        status=invoice_data.status
    )
    invoice_id = await database.execute(query)

    # Récupération de l'élément créé pour retour complet
    fetch_query = invoices.select().where(invoices.c.id == invoice_id)
    invoice = await database.fetch_one(fetch_query)
    return invoice

async def get_invoices_by_user(user_id: int):
    query = invoices.select().where(invoices.c.user_id == user_id).order_by(invoices.c.created_at.desc())
    return await database.fetch_all(query)
