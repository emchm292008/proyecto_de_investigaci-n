# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Configuración de base de datos PostgreSQL
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "investigacion")
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "investigacion")
    
    # Conexión CON SSL (requerido por Neon)
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"
        )

# Instancia global
settings = Settings()
