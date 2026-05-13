"""
fabrica_repositorios.py — Factory centralizada para PostgreSQL.

Crea el repositorio y servicio CRUD para PostgreSQL.
"""

from servicios.conexion.proveedor_conexion import ProveedorConexion
from servicios.servicio_crud import ServicioCrud
from repositorios.repositorio_lectura_postgresql import RepositorioLecturaPostgreSQL


def crear_servicio_crud() -> ServicioCrud:
    """Crea el servicio CRUD con el repositorio PostgreSQL."""
    proveedor = ProveedorConexion()
    repositorio = RepositorioLecturaPostgreSQL(proveedor)
    return ServicioCrud(repositorio_lectura=repositorio)