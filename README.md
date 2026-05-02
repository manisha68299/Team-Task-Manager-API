# 🗂️ Team Task Manager API

A production-style **REST API** built with **FastAPI** for managing team tasks — featuring JWT authentication, full CRUD operations, filtering, pagination, and analytics.

> Built as a real-world learning project to master FastAPI from scratch.

---

## 📌 The Problem

Teams without a centralized task system lose work in Slack threads, miss deadlines, and have no visibility into who is doing what. This API solves that with a clean, secure backend that any frontend or mobile app can plug into.

---

## ✨ Features

- 🔐 **JWT Authentication** — secure registration, login, and protected routes
- ✅ **Full Task CRUD** — create, read, update (PATCH), and delete tasks
- 🔍 **Filtering & Search** — filter by status, priority, or search by title
- 📄 **Pagination** — `skip` and `limit` query params on all list endpoints
- 📊 **Task Analytics** — per-user stats grouped by status
- 🛡️ **Data Validation** — Pydantic schemas validate every request and response
- ⚡ **Performance Header** — every response includes `X-Process-Time`
- 🌐 **CORS Ready** — configured for frontend integration

---

## 🏗️ Project Structure

```
task_manager/
├── main.py              # App entry point, middleware, router wiring
├── database.py          # SQLAlchemy engine + session dependency
├── models.py            # Database table definitions (ORM)
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # Password hashing + JWT token logic
├── routers/
│   ├── __init__.py
│   ├── users.py         # /users routes (register, login, profile)
│   └── tasks.py         # /tasks routes (CRUD, filter, stats)
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`

---

## 📖 Interactive Docs

FastAPI generates documentation automatically:

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI — interactive, try every endpoint |
| `http://localhost:8000/redoc` | ReDoc — clean readable reference |

---

## 🔑 Authentication Flow

```
1. POST /users/register   →  Create your account
2. POST /users/login      →  Get your Bearer token
3. Click "Authorize" in /docs, enter: Bearer <your_token>
4. All protected endpoints now work
```

In your own client (React, mobile, curl, etc.):
```
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints

### Users

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/users/register` | ❌ | Register a new account |
| `POST` | `/users/login` | ❌ | Login and get JWT token |
| `GET` | `/users/me` | ✅ | Get your own profile |
| `GET` | `/users/{user_id}` | ✅ | Get another user's profile |

### Tasks

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/tasks/` | ✅ | Create a new task |
| `GET` | `/tasks/` | ✅ | List your tasks (with filters) |
| `GET` | `/tasks/stats` | ✅ | Get your task statistics |
| `GET` | `/tasks/{task_id}` | ✅ | Get a specific task |
| `PATCH` | `/tasks/{task_id}` | ✅ | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | ✅ | Delete a task |

---

## 🔍 Query Parameters — GET /tasks/

| Param | Type | Description | Example |
|---|---|---|---|
| `status` | string | Filter by task status | `?status=todo` |
| `is_priority` | bool | Filter by priority flag | `?is_priority=true` |
| `search` | string | Search in task title | `?search=bug` |
| `skip` | int | Pagination offset | `?skip=10` |
| `limit` | int | Max results (1–100) | `?limit=20` |

**Combined example:**
```
GET /tasks/?status=in_progress&is_priority=true&limit=5
```

---

## 📦 Request & Response Examples

### Register
```json
POST /users/register
{
  "email": "alice@example.com",
  "username": "alice",
  "password": "secret123"
}
```

### Login
```
POST /users/login
Content-Type: application/x-www-form-urlencoded

username=alice&password=secret123
```
```json
{ "access_token": "eyJhbGci...", "token_type": "bearer" }
```

### Create Task
```json
POST /tasks/
{
  "title": "Fix login bug",
  "description": "Users get logged out randomly after 10 minutes",
  "is_priority": true
}
```

### Update Task Status
```json
PATCH /tasks/1
{ "status": "in_progress" }
```

### Task Stats Response
```json
GET /tasks/stats
{
  "total": 8,
  "by_status": {
    "todo": 3,
    "in_progress": 2,
    "done": 3
  },
  "user": "alice"
}
```

---

## 🗄️ Data Models

### Task Status Values
```
todo | in_progress | done | cancelled
```

### User
| Field | Type | Notes |
|---|---|---|
| id | int | Auto-generated |
| email | string | Unique, validated |
| username | string | Unique, 3–50 chars |
| is_active | bool | Default: true |
| created_at | datetime | Auto-set |

### Task
| Field | Type | Notes |
|---|---|---|
| id | int | Auto-generated |
| title | string | Required, max 200 chars |
| description | string | Optional, max 1000 chars |
| status | enum | Default: `todo` |
| is_priority | bool | Default: false |
| owner_id | int | Foreign key → User |
| created_at | datetime | Auto-set |
| updated_at | datetime | Auto-updated on change |

---

## 🧰 Tech Stack

| Technology | Role |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM / database layer |
| [SQLite](https://www.sqlite.org/) | Database (dev) |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation |
| [python-jose](https://github.com/mpdavis/python-jose) | JWT token handling |
| [passlib + bcrypt](https://passlib.readthedocs.io/) | Password hashing |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |

---

## 🔒 Security Notes

- Passwords are hashed with **bcrypt** — never stored in plain text
- JWT tokens expire after **30 minutes**
- Login errors use a **generic message** to prevent username enumeration
- Each user can only access and modify **their own tasks**
- `SECRET_KEY` in `auth.py` must be changed to a secure random string in production

Generate a secure key:
```bash
openssl rand -hex 32
```

---

## 🌱 What This Project Covers (FastAPI Concepts)

| Concept | Where |
|---|---|
| `APIRouter` + prefix/tags | `routers/users.py`, `routers/tasks.py` |
| Pydantic validation + `Field()` | `schemas.py` |
| SQLAlchemy ORM + relationships | `models.py` |
| `Depends()` dependency injection | All routes |
| `yield` dependencies (cleanup) | `database.py` |
| JWT auth + OAuth2PasswordBearer | `auth.py` |
| Path, Query, Body parameters | `routers/tasks.py` |
| `PATCH` with `exclude_unset=True` | `tasks.py` → `update_task` |
| HTTP status codes (201, 204, 409…) | All routes |
| CORS middleware | `main.py` |
| Custom middleware | `main.py` |
| Global exception handler | `main.py` |
| Aggregate DB queries (`GROUP BY`) | `tasks.py` → `get_my_task_stats` |
| Route ordering (static before param) | `tasks.py` → `/stats` before `/{id}` |


