"""Proveedor de conexión para PostgreSQL desde config.py."""

from config import settings


class ProveedorConexion:
    """Lee la configuración y entrega la cadena de conexión para PostgreSQL."""

    def __init__(self):
        self._settings = settings

    @property
    def proveedor_actual(self) -> str:
        """Proveedor activo: siempre postgresql."""
        return "postgresql"

    def obtener_cadena_conexion(self) -> str:
        """Cadena de conexión async para PostgreSQL con SSL obligatorio."""
        return (
            f"postgresql+asyncpg://"
            f"{self._settings.DB_USER}:{self._settings.DB_PASSWORD}"
            f"@{self._settings.DB_HOST}:{self._settings.DB_PORT}"
            f"/{self._settings.DB_NAME}?sslmode=require"
        )
