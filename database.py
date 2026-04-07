from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Render entrega URLs que empiezan con 'postgres://', pero SQLAlchemy v1.4+ requiere 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    raise ValueError("❌ Error: La variable de entorno DATABASE_URL no está configurada o es inválida.")

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