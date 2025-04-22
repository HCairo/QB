from fastapi import FastAPI
from app.db.database import database, metadata, engine
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # Créer les tables si elles n'existent pas
    metadata.create_all(engine)
    # Connexion à la base
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router)