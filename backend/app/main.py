"""Punto de entrada del backend: crea la app, la BD y registra los controladores."""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.controllers import comision_controller
from app.core.database import Base, SessionLocal, engine
from app.seed import cargar_datos

# Carpeta donde Vite deja el build de React (frontend/dist)
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Al arrancar: crea las tablas y carga los datos de prueba si la BD está vacía."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        cargar_datos(db)
    yield


app = FastAPI(title="MiniCore - Comisiones de vendedores", lifespan=lifespan)

# En desarrollo React corre en http://localhost:5173 y llama a la API en el puerto 8000.
origenes = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origenes, allow_methods=["GET"], allow_headers=["*"])

app.include_router(comision_controller.router)

# En producción (Render) FastAPI también sirve la página de React ya compilada.
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/", include_in_schema=False)
    def frontend():
        return FileResponse(FRONTEND_DIST / "index.html")
