import os
from fastapi import FastAPI
from app.db.database import database, metadata, engine
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.config import stripe
from app.api.auth_google import router as google_auth_router
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Middleware Session (pour OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    same_site="none",
    https_only=False
)

# Inclusion des routes
app.include_router(router)
app.include_router(google_auth_router)

@app.on_event("startup")
async def startup():
    metadata.create_all(engine)
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()