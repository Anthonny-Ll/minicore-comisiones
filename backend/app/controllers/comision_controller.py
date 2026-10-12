"""CONTROLADOR: rutas de la API del MiniCore (vendedores, ventas, reglas y comisiones)."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import regla_model, vendedor_model, venta_model
from app.schemas import ComisionVendedor, ReglaOut, ReporteComisiones, VendedorOut, VentaOut

router = APIRouter(prefix="/api", tags=["MiniCore"])


def validar_rango(inicio: date, fin: date) -> None:
    if fin < inicio:
        raise HTTPException(400, "La fecha fin no puede ser menor que la fecha inicio")


@router.get("/vendedores", response_model=list[VendedorOut])
def listar_vendedores(db: Session = Depends(get_db)):
    return vendedor_model.listar(db)


@router.get("/reglas", response_model=list[ReglaOut])
def listar_reglas(db: Session = Depends(get_db)):
    return regla_model.listar(db)


@router.get("/ventas", response_model=list[VentaOut])
def listar_ventas(
    fecha_inicio: date = Query(..., description="AAAA-MM-DD"),
    fecha_fin: date = Query(..., description="AAAA-MM-DD"),
    db: Session = Depends(get_db),
):
    """Detalle de las ventas dentro del rango de fechas."""
    validar_rango(fecha_inicio, fecha_fin)
    return [
        VentaOut(id=v.id, fecha=v.fecha, monto=v.monto, vendedor_id=v.vendedor_id, vendedor=v.vendedor.nombre)
        for v in venta_model.listar_por_rango(db, fecha_inicio, fecha_fin)
    ]


@router.get("/comisiones", response_model=ReporteComisiones)
def calcular_comisiones(
    fecha_inicio: date = Query(..., description="AAAA-MM-DD"),
    fecha_fin: date = Query(..., description="AAAA-MM-DD"),
    db: Session = Depends(get_db),
):
    """EL CORE: suma las ventas de cada vendedor en el rango y aplica la regla que corresponde."""
    validar_rango(fecha_inicio, fecha_fin)
    totales = venta_model.totales_por_vendedor(db, fecha_inicio, fecha_fin)

    resultados = []
    for vendedor in vendedor_model.listar(db):
        total, cantidad = totales.get(vendedor.id, (0.0, 0))
        regla = regla_model.regla_para(db, total)
        porcentaje = regla.porcentaje if regla else 0.0
        resultados.append(ComisionVendedor(
            vendedor_id=vendedor.id,
            vendedor=vendedor.nombre,
            cantidad_ventas=cantidad,
            total_ventas=round(total, 2),
            regla=regla.nombre if regla else None,
            porcentaje=porcentaje,
            comision=round(total * porcentaje, 2),
        ))

    return ReporteComisiones(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        resultados=resultados,
        total_ventas=round(sum(r.total_ventas for r in resultados), 2),
        total_comisiones=round(sum(r.comision for r in resultados), 2),
    )
