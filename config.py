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
    DB_NAME: str = os.getenv("DB_NAME", "investigation")   # ← nombre correcto
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "public")

    @property
    def DATABASE_URL(self) -> str:
        # Construir URL base
        url = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        # Agregar sslmode=require SOLO si el host NO es localhost o 127.0.0.1
        if self.DB_HOST not in ("localhost", "127.0.0.1"):
            url += "?sslmode=require"
        
        return url

# Instancia global
settings = Settings()
