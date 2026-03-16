from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def test_connection():
    """Verificar la conexión a la base de datos"""
    try:
        with engine.connect() as conn:
            print("✅ ¡Conexión exitosa a PostgreSQL!")
            return True
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return False

if __name__ == "__main__":
    test_connection()