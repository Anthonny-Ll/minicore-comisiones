"""Formas de los datos que devuelve la API (lo que recibe React en JSON)."""
from datetime import date

from pydantic import BaseModel, ConfigDict


class VendedorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    email: str


class ReglaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    monto_minimo: float
    porcentaje: float


class VentaOut(BaseModel):
    id: int
    fecha: date
    monto: float
    vendedor_id: int
    vendedor: str


class ComisionVendedor(BaseModel):
    vendedor_id: int
    vendedor: str
    cantidad_ventas: int
    total_ventas: float
    regla: str | None
    porcentaje: float
    comision: float


class ReporteComisiones(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    resultados: list[ComisionVendedor]
    total_ventas: float
    total_comisiones: float
