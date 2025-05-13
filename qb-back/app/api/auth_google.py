from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from app.db.models import get_user_by_email, create_user_google
from app.security.auth import create_access_token
from starlette.responses import RedirectResponse
import os

router = APIRouter()

# Config OAuth Google
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Redirection vers Google Login
@router.get("/auth/google")
async def login_via_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Callback après validation Google
@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        email = user_info['email']
        name = user_info['name']

        # Vérifie si l'utilisateur existe
        user = await get_user_by_email(email)

        if not user:
            # Crée l'utilisateur si inexistant (fonction à créer si besoin)
            user = await create_user_google(email=email, name=name)

        # Générer le JWT
        jwt_token = create_access_token(data={"sub": str(user["id"])})

        redirect_url = f"http://localhost:5173/oauth-success?token={jwt_token}"
        return RedirectResponse(url=redirect_url)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur OAuth Google : {str(e)}")