"""MODELO: Venta. Tabla 'ventas' (cada venta pertenece a un vendedor)."""
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.core.database import Base


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, index=True)
    monto: Mapped[float] = mapped_column(Float)
    vendedor_id: Mapped[int] = mapped_column(ForeignKey("vendedores.id"))

    vendedor: Mapped["Vendedor"] = relationship(back_populates="ventas")  # noqa: F821


class VentaModel:
    def listar_por_rango(self, db: Session, inicio: date, fin: date) -> list[Venta]:
        """Ventas cuya fecha está entre inicio y fin (ambas incluidas)."""
        consulta = (
            select(Venta)
            .where(Venta.fecha.between(inicio, fin))
            .order_by(Venta.fecha, Venta.id)
        )
        return list(db.scalars(consulta))

    def totales_por_vendedor(self, db: Session, inicio: date, fin: date) -> dict[int, tuple[float, int]]:
        """Devuelve {vendedor_id: (suma de montos, número de ventas)} dentro del rango."""
        consulta = (
            select(Venta.vendedor_id, func.sum(Venta.monto), func.count(Venta.id))
            .where(Venta.fecha.between(inicio, fin))
            .group_by(Venta.vendedor_id)
        )
        return {vid: (float(total), cantidad) for vid, total, cantidad in db.execute(consulta)}


venta_model = VentaModel()
