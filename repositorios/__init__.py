"""Paquete de repositorios — Implementaciones de acceso a datos (solo PostgreSQL)."""

from .repositorio_lectura_postgresql import RepositorioLecturaPostgreSQL

__all__ = [
    "RepositorioLecturaPostgreSQL",
]