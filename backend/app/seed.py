"""Datos de prueba. Solo se insertan si la base está vacía."""
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Regla, Vendedor, Venta

VENDEDORES = [
    ("Carlos Andrade", "carlos@minicore.com"),
    ("María Torres", "maria@minicore.com"),
    ("Juan Pérez", "juan@minicore.com"),
    ("Ana Morales", "ana@minicore.com"),
]

# Tramos de comisión: se aplica el del monto_minimo más alto que alcance el total.
REGLAS = [
    ("Bronce", 500, 0.06),
    ("Plata", 600, 0.08),
    ("Oro", 800, 0.10),
    ("Diamante", 1000, 0.15),
]

# (vendedor_id, fecha, monto)
VENTAS = [
    (1, date(2026, 8, 3), 400.00),
    (2, date(2026, 8, 10), 600.00),
    (2, date(2026, 8, 21), 200.00),
    (1, date(2026, 8, 28), 300.00),
    (3, date(2026, 9, 2), 900.00),
    (4, date(2026, 9, 8), 1000.00),
    (1, date(2026, 9, 15), 1200.00),
    (2, date(2026, 9, 22), 800.00),
    (3, date(2026, 9, 29), 150.00),
    (4, date(2026, 10, 1), 700.00),
    (3, date(2026, 10, 5), 500.00),
    (1, date(2026, 10, 8), 250.00),
]


def cargar_datos(db: Session) -> None:
    if db.scalar(select(Vendedor).limit(1)):
        return  # ya hay datos
    db.add_all(Vendedor(nombre=n, email=e) for n, e in VENDEDORES)
    db.add_all(Regla(nombre=n, monto_minimo=m, porcentaje=p) for n, m, p in REGLAS)
    db.flush()
    db.add_all(Venta(vendedor_id=v, fecha=f, monto=m) for v, f, m in VENTAS)
    db.commit()
