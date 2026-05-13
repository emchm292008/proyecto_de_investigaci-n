"""
Controlador específico para la base de datos de investigación
Proporciona endpoints optimizados para las 19 tablas del sistema
"""
from typing import Optional, Any
from fastapi import APIRouter, HTTPException, Query, Depends, Body
from servicios.fabrica_repositorios import crear_servicio_crud

router = APIRouter(prefix="/api/investigacion", tags=["Investigación"])

TABLAS_VALIDAS = [
    "area_conocimiento", "objetivo_desarrollo_sostenible", "area_aplicacion",
    "termino_clave", "universidad", "linea_investigacion", "docente",
    "grupo_investigacion", "semillero", "participa_semillero",
    "participa_grupo", "semillero_linea", "grupo_linea", "ac_linea",
    "ods_linea", "aa_linea",
    "rol", "usuario", "rol_usuario"
]

ESQUEMA_DEFAULT = "public"

def validar_tabla(tabla: str):
    if tabla not in TABLAS_VALIDAS:
        raise HTTPException(
            status_code=400,
            detail={
                "estado": 400,
                "mensaje": f"Tabla '{tabla}' no válida",
                "tablas_validas": TABLAS_VALIDAS
            }
        )
    return tabla

# =========================================================================
# GET /api/investigacion/{tabla} — Listar registros
# =========================================================================
@router.get("/{tabla}")
async def listar_registros(
    tabla: str = Depends(validar_tabla),
    limite: Optional[int] = Query(None, description="Límite de registros")
):
    try:
        servicio = crear_servicio_crud()
        filas = await servicio.listar(tabla, ESQUEMA_DEFAULT, limite)
        return {
            "estado": 200,
            "tabla": tabla,
            "total": len(filas),
            "datos": filas
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# =========================================================================
# GET /api/investigacion/{tabla}/{clave}/{valor} — Buscar por clave
# =========================================================================
@router.get("/{tabla}/{clave}/{valor}")
async def obtener_por_clave(
    tabla: str = Depends(validar_tabla),
    clave: str = None,
    valor: str = None
):
    try:
        servicio = crear_servicio_crud()
        filas = await servicio.obtener_por_clave(tabla, clave, valor, ESQUEMA_DEFAULT)
        if not filas:
            raise HTTPException(status_code=404, detail=f"No se encontraron registros con {clave}={valor}")
        return {
            "estado": 200,
            "tabla": tabla,
            "filtro": f"{clave}={valor}",
            "total": len(filas),
            "datos": filas
        }
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# =========================================================================
# POST /api/investigacion/{tabla} — Crear registro
# =========================================================================
@router.post("/{tabla}")
async def crear_registro(
    tabla: str = Depends(validar_tabla),
    datos: dict[str, Any] = Body(None)
):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="Datos requeridos")
        servicio = crear_servicio_crud()
        resultado = await servicio.crear(tabla, datos, ESQUEMA_DEFAULT)
        return {
            "estado": 201,
            "mensaje": "Registro creado exitosamente",
            "tabla": tabla
        }
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# =========================================================================
# Endpoints específicos para docentes
# =========================================================================
@router.get("/docentes/por-linea/{linea_id}")
async def docentes_por_linea(linea_id: int):
    try:
        servicio = crear_servicio_crud()
        docentes = await servicio.obtener_por_clave(
            "docente", "linea_investigacion_principal", str(linea_id), ESQUEMA_DEFAULT
        )
        return {
            "estado": 200,
            "linea_investigacion": linea_id,
            "total_docentes": len(docentes),
            "docentes": docentes
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/grupos/por-universidad/{universidad_id}")
async def grupos_por_universidad(universidad_id: int):
    try:
        servicio = crear_servicio_crud()
        grupos = await servicio.obtener_por_clave(
            "grupo_investigacion", "universidad", str(universidad_id), ESQUEMA_DEFAULT
        )
        return {
            "estado": 200,
            "universidad_id": universidad_id,
            "total_grupos": len(grupos),
            "grupos": grupos
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))