"""
Controlador de autenticación.
Endpoint: POST /api/usuario/verificar-contrasena
"""

from fastapi import APIRouter, HTTPException, Query
from servicios.fabrica_repositorios import crear_servicio_crud
from servicios.utilidades.encriptacion_bcrypt import verificar

router = APIRouter()


@router.post("/usuario/verificar-contrasena")
async def verificar_contrasena(
    campo_usuario: str = Query(...),
    campo_contrasena: str = Query(...),
    valor_usuario: str = Query(...),
    valor_contrasena: str = Query(...),
    esquema: str = Query("public")
):
    """
    Verifica credenciales de un usuario.
    Parámetros (query string):
      - campo_usuario: nombre de la columna de usuario (ej. 'username')
      - campo_contrasena: nombre de la columna de contraseña (ej. 'password')
      - valor_usuario: valor ingresado en el login
      - valor_contrasena: contraseña ingresada en el login
      - esquema: esquema de la BD (por defecto 'public')
    """
    try:
        servicio = crear_servicio_crud()
        repositorio = servicio.repositorio_lectura

        # Obtener el hash almacenado en la BD
        hash_almacenado = await repositorio.obtener_hash_contrasena(
            nombre_tabla="usuario",
            campo_usuario=campo_usuario,
            campo_contrasena=campo_contrasena,
            valor_usuario=valor_usuario,
            esquema=esquema
        )

        if not hash_almacenado:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Comparar contraseña con el hash
        if verificar(valor_contrasena, hash_almacenado):
            return {"estado": 200, "mensaje": "Autenticación exitosa"}
        else:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))