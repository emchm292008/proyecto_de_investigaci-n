"""Paquete de modelos Pydantic para las 19 tablas del sistema de investigación."""

from .entidades import (
    AreaConocimiento,
    ObjetivoDesarrolloSostenible,
    AreaAplicacion,
    TerminoClave,
    Universidad,
    LineaInvestigacion,
    Docente,
    GrupoInvestigacion,
    Semillero,
    ParticipaSemillero,
    ParticipaGrupo,
    SemilleroLinea,
    GrupoLinea,
    AcLinea,
    OdsLinea,
    AaLinea,
    Rol,
    Usuario,
    RolUsuario
)

__all__ = [
    "AreaConocimiento",
    "ObjetivoDesarrolloSostenible",
    "AreaAplicacion",
    "TerminoClave",
    "Universidad",
    "LineaInvestigacion",
    "Docente",
    "GrupoInvestigacion",
    "Semillero",
    "ParticipaSemillero",
    "ParticipaGrupo",
    "SemilleroLinea",
    "GrupoLinea",
    "AcLinea",
    "OdsLinea",
    "AaLinea",
    "Rol",
    "Usuario",
    "RolUsuario"
]