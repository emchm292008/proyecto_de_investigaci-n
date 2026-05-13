from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from controllers import entidades_controller, investigacion_controller
from controllers.auth_controller import router as auth_router

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

# Registrar ambos controladores
app.include_router(entidades_controller)          # /api/{tabla}
app.include_router(investigacion_controller)      # /api/investigacion/{tabla}
app.include_router(auth_router, prefix="/api")  # ← NUEVO

@app.get("/", tags=["Diagnóstico"])
async def root():
    return {
        "mensaje": "API Investigación funcionando",
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