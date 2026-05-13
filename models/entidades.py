"""
Modelos Pydantic para las 19 tablas de la base de datos investigación
"""
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field


# ============================================
# TABLAS DEL MÓDULO: INVESTIGACIÓN
# ============================================

class AreaConocimiento(BaseModel):
    id: Optional[int] = None        
    gran_area: str = Field(max_length=60)
    area: str = Field(max_length=60)
    disciplina: str = Field(max_length=60)

class ObjetivoDesarrolloSostenible(BaseModel):
    id: int
    nombre: str = Field(max_length=60)
    categoria: str = Field(max_length=45)

class AreaAplicacion(BaseModel):
    id: int
    nombre: str = Field(max_length=60)

class TerminoClave(BaseModel):
    termino: str = Field(max_length=30)
    termino_ingles: Optional[str] = Field(None, max_length=30)

class Universidad(BaseModel):
    id: int
    nombre: str = Field(max_length=60)
    tipo: str = Field(max_length=45)
    ciudad: str = Field(max_length=45)

class LineaInvestigacion(BaseModel):
    nombre: str = Field(max_length=45)
    descripcion: str = Field(max_length=256)

class Docente(BaseModel):
    cedula: int
    nombres: str = Field(max_length=60)
    apellidos: str = Field(max_length=60)
    genero: str = Field(max_length=12)
    cargo: str = Field(max_length=30)
    fecha_nacimiento: date
    correo: str = Field(max_length=70)
    telefono: str = Field(max_length=20)
    url_cvlac: str = Field(max_length=128)
    fecha_actualizacion: date
    escalafon: str = Field(max_length=45)
    perfil: str
    cat_minciencia: Optional[str] = Field(None, max_length=45)
    conv_minciencia: str = Field(max_length=45)
    nacionalidad: str = Field(max_length=45)
    linea_investigacion_principal: Optional[int] = None

class GrupoInvestigacion(BaseModel):
    id: int
    nombre: str = Field(max_length=60)
    url_gruplac: Optional[str] = Field(None, max_length=128)
    categoria: Optional[str] = Field(None, max_length=10)
    convocatoria: Optional[str] = Field(None, max_length=10)
    fecha_fundacion: date
    universidad: Optional[int] = None
    interno: int = Field(ge=0, le=1)  # SMALLINT
    ambito: str = Field(max_length=45)

class Semillero(BaseModel):
    id: int
    nombre: str = Field(max_length=60)
    fecha_fundacion: date
    grupo_investigacion: int

class ParticipaSemillero(BaseModel):
    docente: int
    semillero: int
    rol: str = Field(max_length=15)
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class ParticipaGrupo(BaseModel):
    docente_cedula: int
    grupo_investigacion_id: int
    rol: str = Field(max_length=15)
    fecha_inicio: date
    fecha_fin: Optional[date] = None

# Tablas de relación muchos a muchos
class SemilleroLinea(BaseModel):
    semillero: int
    linea_investigacion: int

class GrupoLinea(BaseModel):
    grupo_investigacion: int
    linea_investigacion: int

class AcLinea(BaseModel):
    linea_investigacion: int
    area_conocimiento: int

class OdsLinea(BaseModel):
    linea_investigacion: int
    ods: int

class AaLinea(BaseModel):
    area_aplicacion: int
    linea_investigacion: int

# ============================================
# MÓDULO DE GESTIÓN DE USUARIOS
# ============================================

class Rol(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class Usuario(BaseModel):
    username: str = Field(max_length=100)
    password: str = Field(max_length=255)
    email: str = Field(max_length=150)
    nombre_completo: Optional[str] = Field(None, max_length=200)
    activo: Optional[bool] = True

class RolUsuario(BaseModel):
    usuario_id: int
    rol_id: int