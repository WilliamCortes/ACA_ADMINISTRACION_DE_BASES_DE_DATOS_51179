# Library API

API REST para gestión de biblioteca: usuarios, libros y préstamos.

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Git

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Django 4.2 + Django REST Framework |
| Base de datos | PostgreSQL 15 |
| Cliente DB | Adminer (puerto 8080) |
| Documentación | Swagger UI — drf-spectacular |
| Contenedores | Docker + Docker Compose |

---

## Estructura del proyecto

```
library_project/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── .env.example
├── library_project/
│   ├── settings.py
│   └── urls.py
└── apps/
    ├── users/       → modelo, serializer, repository, service, view, urls
    ├── books/       → modelo, serializer, repository, service, view, urls
    └── borrows/     → modelo, serializer, repository, service, view, urls
```

Cada app sigue el patrón **Repository → Service → View**:
- `repositories.py` — solo queries al ORM
- `services.py` — lógica de negocio
- `views.py` — recibe la request, delega al service, retorna la respuesta

---

## Configuración inicial (solo la primera vez)

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd library_project
```

### 2. Crear el archivo de variables de entorno

```bash
cp .env.example .env
```

> No es necesario cambiar nada para correrlo en local. Los valores por defecto funcionan.

### 3. Levantar los contenedores

```bash
docker compose up -d
```

Esto levanta tres servicios:
- `web` → Django en `http://localhost:8000`
- `db` → PostgreSQL en el puerto 5432
- `adminer` → cliente web para la DB en `http://localhost:8080`

### 4. Crear las tablas en la base de datos

```bash
docker compose exec web python manage.py makemigrations users books borrows
docker compose exec web python manage.py migrate
```

### 5. Cargar datos de prueba (100 libros)

```bash
docker compose exec web python manage.py loaddata seed_books.json
```

### 6. Crear superusuario para el panel de administración

```bash
docker compose exec web python manage.py createsuperuser
```

Sigue las instrucciones en pantalla (nombre, email, contraseña).

---

## URLs del proyecto

| URL | Descripción |
|---|---|
| `http://localhost:8000/api/users/` | CRUD de usuarios |
| `http://localhost:8000/api/books/` | CRUD de libros |
| `http://localhost:8000/api/borrows/` | Gestión de préstamos |
| `http://localhost:8000/api/docs/` | Documentación Swagger |
| `http://localhost:8000/admin/` | Panel de administración Django |
| `http://localhost:8080` | Adminer — cliente web de la DB |

---

## Endpoints principales

### Usuarios — `/api/users/`

| Método | URL | Acción |
|---|---|---|
| GET | `/api/users/` | Listar usuarios |
| POST | `/api/users/` | Crear usuario |
| GET | `/api/users/{id}/` | Ver usuario |
| PUT | `/api/users/{id}/` | Actualizar usuario |
| DELETE | `/api/users/{id}/` | Eliminar usuario |

### Libros — `/api/books/`

| Método | URL | Acción |
|---|---|---|
| GET | `/api/books/` | Listar libros |
| POST | `/api/books/` | Crear libro |
| GET | `/api/books/{id}/` | Ver libro |
| PUT | `/api/books/{id}/` | Actualizar libro |
| DELETE | `/api/books/{id}/` | Eliminar libro |

### Préstamos — `/api/borrows/`

| Método | URL | Acción |
|---|---|---|
| GET | `/api/borrows/` | Listar préstamos |
| GET | `/api/borrows/{id}/` | Ver préstamo |
| POST | `/api/borrows/create_borrow/` | Crear préstamo |
| PATCH | `/api/borrows/{id}/return_book/` | Devolver libro |

#### Body para crear un préstamo

```json
{
  "user": 1,
  "book": 1,
  "due_date": "2025-12-31"
}
```

---

## Reglas de negocio

- **Crear préstamo:** el libro debe tener `stock > 0`. Al crearse, el stock baja en 1.
- **Devolver libro:** el préstamo no puede estar ya en estado `RETURNED`. Al devolverse, el stock sube en 1 y se registra la `return_date`.
- **Estados posibles:** `BORROWED` · `RETURNED` · `LATE`

---

## Acceso a Adminer (`http://localhost:8080`)

| Campo | Valor |
|---|---|
| Sistema | PostgreSQL |
| Servidor | `db` |
| Usuario | `library_user` |
| Contraseña | `library_pass` |
| Base de datos | `library_db` |

---

## Comandos útiles

```bash
# Ver logs de la app
docker compose logs -f web

# Detener todos los servicios
docker compose down

# Detener y borrar la base de datos (reset total)
docker compose down -v

# Abrir una shell dentro del contenedor
docker compose exec web bash
```

---

## Variables de entorno (`.env`)

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | `change-me-in-production` |
| `DJANGO_DEBUG` | Modo debug | `True` |
| `DB_NAME` | Nombre de la base de datos | `library_db` |
| `DB_USER` | Usuario de PostgreSQL | `library_user` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `library_pass` |
| `DB_HOST` | Host de la DB | `db` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |

> En producción cambiar `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` y las credenciales de la DB.
