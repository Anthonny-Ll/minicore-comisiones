// Funciones que llaman a la API de FastAPI. React nunca toca la base de datos directamente.

async function pedir(ruta) {
  const res = await fetch(ruta)
  const datos = await res.json()
  if (!res.ok) throw new Error(datos.detail || 'Error al consultar el servidor')
  return datos
}

export const obtenerReglas = () => pedir('/api/reglas')

export const obtenerComisiones = (inicio, fin) =>
  pedir(`/api/comisiones?fecha_inicio=${inicio}&fecha_fin=${fin}`)

export const obtenerVentas = (inicio, fin) =>
  pedir(`/api/ventas?fecha_inicio=${inicio}&fecha_fin=${fin}`)
