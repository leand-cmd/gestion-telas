# LUCMA — Sistema de Gestión de Ventas de Telas

Aplicación de gestión de ventas para empresa de telas. Backend Flask + PostgreSQL, frontend React + TypeScript.

## Módulos

- Autenticación (JWT) y gestión de Usuarios (roles: Admin, Gerente, Asesor Comercial, Vendedor)
- Clientes (CRUD, geolocalización, importación/exportación masiva)
- Productos (CRUD, imagen, importación/exportación masiva)
- Pedidos (líneas de detalle, numeración correlativa, PDF, envío por email, conversión manual a Venta)
- Ventas (carga suelta o desde un pedido, estado de pago, PDF)
- Stock (movimientos manuales de entrada/salida/ajuste, alertas de stock bajo mínimo)
- Visitas y Agenda (programación, registro de resultado)
- Dashboard (ventas por mes, pedidos pendientes, stock bajo, top clientes/productos)
- Importación masiva unificada (Clientes/Productos desde una sola pantalla)

## Stack

- **Backend**: Flask, SQLAlchemy, Flask-Migrate (Alembic), Flask-JWT-Extended, marshmallow, reportlab (PDF), pandas/openpyxl (import/export)
- **Frontend**: React + TypeScript + Vite, TanStack Query, React Router
- **Base de datos**: PostgreSQL (SQLite como fallback local)

## Requisitos previos

- Python 3.12+
- Node.js 20+
- Una base de datos PostgreSQL (recomendado: Railway)

---

## Desarrollo local

### Backend

```bash
cd backend
python -m venv venv
./venv/Scripts/activate        # Windows
pip install -r requirements-dev.txt
cp .env.example .env           # completar DATABASE_URL con la connection string de Railway
flask db upgrade                # crea/actualiza las tablas del esquema
flask run                       # http://localhost:5000
```

Correr los tests (usan SQLite en memoria, no tocan la base real):

```bash
pytest
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_URL, opcionalmente VITE_GOOGLE_MAPS_API_KEY
npm run dev                     # http://localhost:5173
```

Sin `VITE_GOOGLE_MAPS_API_KEY`, el formulario de clientes usa campos manuales de latitud/longitud en lugar del mapa interactivo.

---

## Despliegue en Railway

Cada servicio se despliega por separado, sin Docker — Railway detecta el proyecto Python/Node con **Railpack** y usa el `Procfile`/`package.json` de cada carpeta como comando de arranque.

1. **Base de datos**: en el proyecto de Railway, agregar el plugin **PostgreSQL**. Railway genera automáticamente la variable `DATABASE_URL` (referenciable desde otros servicios como `${{Postgres.DATABASE_URL}}`).

2. **Backend**: crear un servicio nuevo apuntando a este repo, con **Root Directory = `backend`**. Variables de entorno:
   - `DATABASE_URL` → referencia a la del plugin de Postgres
   - `SECRET_KEY`, `JWT_SECRET_KEY` → strings aleatorios largos
   - `CORS_ORIGINS` → la URL pública que Railway asigne al frontend
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `EMAIL_COLABORADORES` → si se quiere habilitar el envío de pedidos por email
   - `GOOGLE_MAPS_API_KEY`, `GOOGLE_CALENDAR_CLIENT_ID`, `GOOGLE_CALENDAR_CLIENT_SECRET` → opcionales
   - `CLOUDINARY_URL` → opcional, para las imágenes de productos

   El `Procfile` (`web: flask db upgrade && gunicorn --bind 0.0.0.0:$PORT wsgi:app`) corre las migraciones pendientes una sola vez, antes de levantar `gunicorn`, en cada deploy.

3. **Frontend**: crear otro servicio apuntando al mismo repo, con **Root Directory = `frontend`**. Como Vite incrusta las variables `VITE_*` en el build, hay que definirlas como **variables de build** en Railway:
   - `VITE_API_URL` → URL pública del servicio backend + `/api` (ej: `https://lucma-backend-production.up.railway.app/api`)
   - `VITE_GOOGLE_MAPS_API_KEY` → opcional

4. Cada servicio recibe un dominio público `*.up.railway.app` (o un dominio propio si se configura). Railway inyecta `PORT` automáticamente.

---

## Estructura

```
backend/    API Flask (modelos, esquema completo de BD, endpoints REST, Procfile)
frontend/   SPA React + TypeScript (Vite)
```
