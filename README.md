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
- Una base de datos PostgreSQL (recomendado: Railway) o Docker

---

## Opción A — Desarrollo local sin Docker

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

## Opción B — Desarrollo local con Docker Compose

Levanta Postgres + backend + frontend con un solo comando, sin instalar Python/Node localmente.

```bash
cp .env.example .env    # completar los valores que necesites (los demás tienen default de desarrollo)
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Postgres: localhost:5432

El frontend, dentro de Docker, llama a `/api` y nginx lo reenvía internamente al contenedor del backend (no hace falta configurar `VITE_API_URL` para este modo).

---

## Despliegue en Railway

Railway **no** orquesta el `docker-compose.yml` — cada servicio se despliega por separado, cada uno leyendo su propio `Dockerfile`. `docker-compose.yml` es solo para desarrollo local (Opción B).

1. **Base de datos**: en el proyecto de Railway, agregar el plugin **PostgreSQL**. Railway genera automáticamente la variable `DATABASE_URL` (referenciable desde otros servicios como `${{Postgres.DATABASE_URL}}`).

2. **Backend**: crear un servicio nuevo apuntando a este repo, con **Root Directory = `backend`** (para que Railway detecte `backend/Dockerfile`). Variables de entorno:
   - `DATABASE_URL` → referencia a la del plugin de Postgres
   - `SECRET_KEY`, `JWT_SECRET_KEY` → strings aleatorios largos
   - `CORS_ORIGINS` → la URL pública que Railway asigne al frontend
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `EMAIL_COLABORADORES` → si se quiere habilitar el envío de pedidos por email
   - `GOOGLE_MAPS_API_KEY`, `GOOGLE_CALENDAR_CLIENT_ID`, `GOOGLE_CALENDAR_CLIENT_SECRET` → opcionales
   - `CLOUDINARY_URL` → opcional, para reemplazar el almacenamiento local de imágenes

   El contenedor corre `flask db upgrade` antes de levantar `gunicorn`, así que las migraciones se aplican en cada deploy.

3. **Frontend**: crear otro servicio apuntando al mismo repo, con **Root Directory = `frontend`** (usa `frontend/Dockerfile`). Como Vite incrusta las variables `VITE_*` en el build, hay que definirlas como **variables de build** en Railway:
   - `VITE_API_URL` → URL pública del servicio backend + `/api` (ej: `https://lucma-backend-production.up.railway.app/api`)
   - `VITE_GOOGLE_MAPS_API_KEY` → opcional

4. Cada servicio recibe un dominio público `*.up.railway.app` (o un dominio propio si se configura). Railway inyecta `PORT` automáticamente; ambos Dockerfiles ya están preparados para escucharlo.

---

## Estructura

```
backend/    API Flask (modelos, esquema completo de BD, endpoints REST, Dockerfile)
frontend/   SPA React + TypeScript (Vite, Dockerfile + nginx)
docker-compose.yml   Orquestación solo para desarrollo local
```
