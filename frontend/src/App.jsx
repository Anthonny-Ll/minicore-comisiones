import { useEffect, useState } from 'react'
import { obtenerComisiones, obtenerReglas, obtenerVentas } from './api'

const dinero = (n) => n.toLocaleString('es-EC', { style: 'currency', currency: 'USD' })
const pct = (p) => `${(p * 100).toFixed(0)} %`

export default function App() {
  const [inicio, setInicio] = useState('2026-09-01')
  const [fin, setFin] = useState('2026-09-30')
  const [reglas, setReglas] = useState([])
  const [reporte, setReporte] = useState(null)
  const [ventas, setVentas] = useState([])
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(false)

  useEffect(() => {
    obtenerReglas().then(setReglas).catch((e) => setError(e.message))
  }, [])

  async function calcular(e) {
    e.preventDefault()
    setError('')
    if (!inicio || !fin) return setError('Selecciona las dos fechas')
    if (fin < inicio) return setError('La fecha fin no puede ser menor que la fecha inicio')
    setCargando(true)
    try {
      const [rep, vts] = await Promise.all([obtenerComisiones(inicio, fin), obtenerVentas(inicio, fin)])
      setReporte(rep)
      setVentas(vts)
    } catch (err) {
      setError(err.message)
      setReporte(null)
    } finally {
      setCargando(false)
    }
  }

  return (
    <main className="pagina">
      <header>
        <h1>MiniCore · Comisiones de vendedores</h1>
        <p className="sub">Elige un rango de fechas: se suman las ventas de cada vendedor y se aplica la regla de comisión que alcance.</p>
      </header>

      <section className="tarjeta">
        <form className="filtro" onSubmit={calcular} noValidate>
          <label>
            Fecha inicio
            <input type="date" value={inicio} onChange={(e) => setInicio(e.target.value)} />
          </label>
          <label>
            Fecha fin
            <input type="date" value={fin} onChange={(e) => setFin(e.target.value)} />
          </label>
          <button type="submit" disabled={cargando}>{cargando ? 'Calculando…' : 'Calcular comisiones'}</button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>

      <section className="tarjeta">
        <h2>Reglas de comisión</h2>
        <div className="reglas">
          {reglas.map((r) => (
            <div key={r.id} className="regla">
              <strong>{r.nombre}</strong>
              <span>desde {dinero(r.monto_minimo)}</span>
              <span className="badge">{pct(r.porcentaje)}</span>
            </div>
          ))}
        </div>
      </section>

      {reporte && (
        <>
          <section className="tarjeta">
            <h2>Resultado del {reporte.fecha_inicio} al {reporte.fecha_fin}</h2>
            <table>
              <thead>
                <tr>
                  <th>Vendedor</th><th className="num">N.º ventas</th><th className="num">Total vendido</th>
                  <th>Regla</th><th className="num">%</th><th className="num">Comisión</th>
                </tr>
              </thead>
              <tbody>
                {reporte.resultados.map((r) => (
                  <tr key={r.vendedor_id}>
                    <td>{r.vendedor}</td>
                    <td className="num">{r.cantidad_ventas}</td>
                    <td className="num">{dinero(r.total_ventas)}</td>
                    <td>{r.regla ?? <span className="sin">Sin comisión</span>}</td>
                    <td className="num">{pct(r.porcentaje)}</td>
                    <td className="num comision">{dinero(r.comision)}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr>
                  <td colSpan={2}>Totales</td>
                  <td className="num">{dinero(reporte.total_ventas)}</td>
                  <td colSpan={2}></td>
                  <td className="num comision">{dinero(reporte.total_comisiones)}</td>
                </tr>
              </tfoot>
            </table>
          </section>

          <section className="tarjeta">
            <h2>Detalle de ventas en el rango ({ventas.length})</h2>
            {ventas.length === 0 ? (
              <p className="sin">No hay ventas en ese rango.</p>
            ) : (
              <table>
                <thead><tr><th>Fecha</th><th>Vendedor</th><th className="num">Monto</th></tr></thead>
                <tbody>
                  {ventas.map((v) => (
                    <tr key={v.id}><td>{v.fecha}</td><td>{v.vendedor}</td><td className="num">{dinero(v.monto)}</td></tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </>
      )}
    </main>
  )
}
