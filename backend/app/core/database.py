"""Conexión a la base de datos SQLite con SQLAlchemy."""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# El archivo minicore.db se crea solo dentro de la carpeta backend/.
DB_PATH = Path(__file__).resolve().parent.parent.parent / "minicore.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Clase padre de todas las tablas."""


def get_db():
    """Dependencia de FastAPI: abre una sesión de BD por petición y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
