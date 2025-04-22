from app.db.database import engine, metadata

if __name__ == "__main__":
    metadata.create_all(engine)
    print("✅ Tables créées !")
