import subprocess

def run_migrations():
    print("🚀 Iniciando proceso de migración...")
    
    try:
        # 1. Generar la revisión (Detecta cambios en los modelos)
        print("🔍 Detectando cambios en los modelos...")
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "auto"], check=True)
        
        # 2. Aplicar la migración a PostgreSQL
        print("🏗️ Aplicando cambios a la base de datos...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        
        print("✅ ¡Base de datos sincronizada con éxito!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")

if __name__ == "__main__":
    run_migrations()