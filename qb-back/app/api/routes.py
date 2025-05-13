import stripe as stripe_lib
from fastapi import APIRouter, HTTPException, Depends, Path
from app.schemas.user import UserIn, UserOut
from app.schemas.invoice import InvoiceIn, InvoiceOut, InvoiceUpdate
from app.security.password import verify_password
from app.crud.operations import create_user, create_invoice, get_invoices_by_user
from app.db.models import get_user_by_email, invoices, companies
from app.db.database import database
from app.security.auth import create_access_token, get_current_user
from app.config import stripe

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

@router.post("/create-checkout-session")
async def create_checkout_session():
    try:
        # Créer une session de paiement Stripe
        checkout_session = stripe_lib.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Invoice Payment',
                        },
                        'unit_amount': 5000,  # Montant en cents (ex : 5000 = 50.00 USD)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:5173/success',  # URL valide pour le succès
            cancel_url='http://localhost:5173/cancel',   # URL valide pour l'annulation
        )
        return {"sessionId": checkout_session.id} # Rediriger vers l'URL de la session

    except stripe_lib.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe Error: {e.user_message}")
    
@router.post("/profile/company")
async def save_company_info(data: dict, current_user: dict = Depends(get_current_user)):
    query = companies.insert().values(
        user_id=current_user["id"],
        company_name=data["company_name"],
        siret=data.get("siret"),
        sector=data.get("sector")
    )
    await database.execute(query)
    return {"message": "Profil entreprise enregistré"}

# 🚀 Sauvegarde du profil entreprise
@router.post("/profile/company")
async def save_company_info(data: dict, current_user: dict = Depends(get_current_user)):
    query = companies.insert().values(
        user_id=current_user["id"],
        company_name=data["company_name"],
        siret=data.get("siret"),
        sector=data.get("sector")
    )
    await database.execute(query)
    return {"message": "Profil entreprise enregistré"}

# ✅ Vérification si le profil entreprise existe
@router.get("/profile/company")
async def check_company_profile(current_user: dict = Depends(get_current_user)):
    query = companies.select().where(companies.c.user_id == current_user["id"])
    company = await database.fetch_one(query)
    return {"exists": bool(company)}
