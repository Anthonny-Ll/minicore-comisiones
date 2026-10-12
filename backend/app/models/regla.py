"""MODELO: Regla de comisión. Tabla 'reglas'.

Cada regla dice: "si el total vendido es al menos monto_minimo, la comisión es porcentaje".
Ejemplo: monto_minimo=1000, porcentaje=0.15  ->  15 % de comisión."""
from sqlalchemy import Float, Integer, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.core.database import Base


class Regla(Base):
    __tablename__ = "reglas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    monto_minimo: Mapped[float] = mapped_column(Float)
    porcentaje: Mapped[float] = mapped_column(Float)  # 0.15 = 15 %


class ReglaModel:
    def listar(self, db: Session) -> list[Regla]:
        return list(db.scalars(select(Regla).order_by(Regla.monto_minimo)))

    def regla_para(self, db: Session, total: float) -> Regla | None:
        """La regla con el monto_minimo más alto que el total alcanza. None si no llega a ninguna."""
        consulta = (
            select(Regla)
            .where(Regla.monto_minimo <= total)
            .order_by(Regla.monto_minimo.desc())
            .limit(1)
        )
        return db.scalar(consulta)


regla_model = ReglaModel()
