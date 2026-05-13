from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from controllers import entidades_controller, investigacion_controller
from servicios.fabrica_repositorios import crear_servicio_crud
from servicios.utilidades.encriptacion_bcrypt import verificar

app = FastAPI(
    title="API Investigación - PostgreSQL",
    description="API REST para operaciones CRUD sobre las 19 tablas del sistema de investigación",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# ENDPOINT DE DIAGNÓSTICO (prueba de vida)
# ------------------------------------------------------------
@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "API funcionando correctamente"}

# ------------------------------------------------------------
# ENDPOINT DE DIAGNÓSTICO DE URL DE CONEXIÓN (verificar SSL y credenciales)
# ------------------------------------------------------------
@app.get("/debug-db-url")
async def debug_db_url():
    from servicios.conexion.proveedor_conexion import ProveedorConexion
    proveedor = ProveedorConexion()
    url = proveedor.obtener_cadena_conexion()
    # Ofuscar contraseña por seguridad
    parts = url.split("://")[1].split("@")
    user_pass = parts[0].split(":")
    password = user_pass[1] if len(user_pass) > 1 else ""
    masked_password = password[:4] + "****" + password[-4:] if len(password) > 8 else "****"
    url_masked = url.replace(password, masked_password) if password else url
    return {
        "url_used_masked": url_masked,
        "db_user": proveedor._settings.DB_USER,
        "db_host": proveedor._settings.DB_HOST,
        "db_name": proveedor._settings.DB_NAME,
        "ssl_param": "ssl=require" in url
    }

# ------------------------------------------------------------
# ENDPOINT DE PRUEBA DE INSERT DIRECTO CON ASYNCPG (sin repositorio)
# ------------------------------------------------------------
@app.post("/test-insert-directo")
async def test_insert_directo():
    from config import settings
    import asyncpg
    url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?ssl=require"
    try:
        conn = await asyncpg.connect(url)
        await conn.execute(
            "INSERT INTO public.usuario (username, password, email) VALUES ($1, $2, $3)",
            "test_api_directo", "clave123", "test@api.com"
        )
        await conn.close()
        return {"ok": True, "message": "INSERT exitoso"}
    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------
# ENDPOINT DE VERIFICACIÓN DE CONTRASEÑA (directo en main)
# ------------------------------------------------------------
@app.post("/api/usuario/verificar-contrasena")
async def verificar_contrasena(
    campo_usuario: str = Query(...),
    campo_contrasena: str = Query(...),
    valor_usuario: str = Query(...),
    valor_contrasena: str = Query(...),
    esquema: str = Query("public")
):
    try:
        servicio = crear_servicio_crud()
        repositorio = servicio.repositorio_lectura

        hash_almacenado = await repositorio.obtener_hash_contrasena(
            nombre_tabla="usuario",
            campo_usuario=campo_usuario,
            campo_contrasena=campo_contrasena,
            valor_usuario=valor_usuario,
            esquema=esquema
        )

        if not hash_almacenado:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if verificar(valor_contrasena, hash_almacenado):
            return {"estado": 200, "mensaje": "Autenticación exitosa"}
        else:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------
# ENDPOINT DE PRUEBA POST (para descartar problemas con imports)
# ------------------------------------------------------------
@app.post("/api/test-login")
async def test_login():
    return {"estado": 200, "mensaje": "Endpoint POST de prueba funcionando"}

# ------------------------------------------------------------
# REGISTRO DE CONTROLADORES (Routers)
# ------------------------------------------------------------
app.include_router(entidades_controller)          # /api/{tabla}
app.include_router(investigacion_controller)      # /api/investigacion/{tabla}

@app.get("/", tags=["Diagnóstico"])
async def root():
    return {
        "mensaje": "API Investigación funcionando - v2 (con ping)",
        "version": "1.0.0",
        "base_datos": settings.DB_NAME,
        "esquema": settings.DB_SCHEMA,
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )