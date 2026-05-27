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
        """
        Cadena de conexión async para PostgreSQL.
        Usa settings.DATABASE_URL (que ya tiene lógica SSL condicional)
        y adapta el esquema a postgresql+asyncpg:// para SQLAlchemy.
        """
        # settings.DATABASE_URL tiene formato postgresql://...
        # Lo cambiamos a postgresql+asyncpg:// para SQLAlchemy async
        base_url = settings.DATABASE_URL
        if base_url.startswith("postgresql://"):
            base_url = base_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return base_url
