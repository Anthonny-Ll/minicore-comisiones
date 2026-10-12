# MiniCore: comisiones de vendedores (FastAPI + React)

Aplicación web que calcula la comisión de cada vendedor según lo que vendió en un rango de fechas.

## Qué hace

1. El usuario elige una **fecha inicio** y una **fecha fin**.
2. El backend suma las ventas de cada vendedor dentro de ese rango.
3. Al total se le aplica la **regla de comisión** con el monto mínimo más alto que alcance:

| Regla    | Desde   | Comisión |
|----------|---------|----------|
| Bronce   | $500    | 6 %      |
| Plata    | $600    | 8 %      |
| Oro      | $800    | 10 %     |
| Diamante | $1000   | 15 %     |

Si el total no llega a $500, la comisión es 0. Ejemplo: María vendió $800 en septiembre, así que le toca la regla Oro: 800 × 10 % = $80.

## Tablas (SQLite)

- **vendedores**: id, nombre, email
- **ventas**: id, fecha, monto, vendedor_id → vendedores.id
- **reglas**: id, nombre, monto_minimo, porcentaje

Un vendedor tiene muchas ventas (1 a N). Las reglas están en la base de datos y no en el código, así que se pueden cambiar sin tocar la lógica.

## Tecnologías

- **Backend:** FastAPI, SQLAlchemy y SQLite, organizado en MVC (models, controllers y schemas)
- **Frontend:** React con Vite (la vista)

## Estructura

```
backend/
  app/
    main.py                         arranque, CORS y servir el build de React
    core/database.py                conexión SQLite
    models/                         vendedor.py, venta.py, regla.py (tablas + consultas)
    controllers/comision_controller.py   rutas /api/...
    schemas.py                      forma del JSON que devuelve la API
    seed.py                         datos de prueba
  requirements.txt
frontend/
  src/App.jsx                       pantalla (filtro, reglas, resultado, detalle)
  src/api.js                        llamadas fetch a la API
  vite.config.js                    proxy /api → puerto 8000 en desarrollo
```

## Cómo ejecutarlo en local

Terminal 1 (backend):
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Terminal 2 (frontend):
```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173. La documentación interactiva de la API está en http://127.0.0.1:8000/docs.

La primera vez se crea `backend/minicore.db` con los datos de prueba (ventas de agosto a octubre de 2026). Para empezar de cero, borra ese archivo.


## Autor

Anthonny Llanos: https://github.com/Anthonny-Ll
