"""MODELO: Vendedor. Tabla 'vendedores'."""
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.core.database import Base


class Vendedor(Base):
    __tablename__ = "vendedores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    # Un vendedor tiene muchas ventas (relación 1 a N)
    ventas: Mapped[list["Venta"]] = relationship(back_populates="vendedor")  # noqa: F821


class VendedorModel:
    def listar(self, db: Session) -> list[Vendedor]:
        return list(db.scalars(select(Vendedor).order_by(Vendedor.id)))


vendedor_model = VendedorModel()
