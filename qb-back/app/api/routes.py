from fastapi import APIRouter, HTTPException, Depends, Path
from app.schemas.user import UserIn, UserOut
from app.schemas.invoice import InvoiceIn, InvoiceOut, InvoiceUpdate
from app.security.password import verify_password
from app.crud.operations import create_user, create_invoice, get_invoices_by_user
from app.db.models import get_user_by_email, invoices
from app.db.database import database
from app.security.auth import create_access_token, get_current_user

router = APIRouter()

# 🚀 Inscription utilisateur
@router.post("/users", response_model=UserOut)
async def register_user(user: UserIn):
    return await create_user(user)

# ✅ Création de facture sécurisée (version clean sans user_id dans l'URL)
@router.post("/invoices", response_model=InvoiceOut)
async def new_invoice(invoice: InvoiceIn, current_user: dict = Depends(get_current_user)):
    return await create_invoice(current_user["id"], invoice)

# 🔐 Login → génération du token JWT
@router.post("/login")
async def login(request: UserIn):
    user = await get_user_by_email(request.email)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user["id"])})
    return {"access_token": token, "token_type": "bearer"}

# 👤 Récupérer les infos du user connecté
@router.get("/me", response_model=UserOut)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/invoices", response_model=list[InvoiceOut])
async def list_invoices(current_user: dict = Depends(get_current_user)):
    return await get_invoices_by_user(current_user["id"])

@router.patch("/invoices/{invoice_id}", response_model=InvoiceOut)
async def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    current_user: dict = Depends(get_current_user)
):
    query = invoices.update().where(
        invoices.c.id == invoice_id,
        invoices.c.user_id == current_user["id"]
    ).values(
        **invoice_data.dict(exclude_unset=True)  # Mettre à jour uniquement les champs modifiés
    )

    await database.execute(query)
    return await database.fetch_one(invoices.select().where(invoices.c.id == invoice_id))

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int, current_user: dict = Depends(get_current_user)):
    query = invoices.delete().where(
        invoices.c.id == invoice_id,
        invoices.c.user_id == current_user["id"]
    )
    await database.execute(query)
    return {"message": "Invoice deleted"}