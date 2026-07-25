# Parcel PaaS

Parcel PaaS is a Platform-as-a-Service designed to import source code (via GitHub OAuth or ZIP archives), dynamically generate build configurations, and deploy isolated application containers using a custom container runtime (`dock`).

---

## System Architecture

The system consists of four main layers:

1. Frontend Layer
   - Minimal Single Page Application built with HTML, CSS, and Vanilla JavaScript.
   - Communicates with the backend using REST APIs.

2. Backend API Layer
   - Built with FastAPI (Python) and SQLAlchemy Async ORM.
   - Handles authentication, OAuth integrations, source downloads, and container operations.
   - Core infrastructure includes `security.py` (password hashing & JWT management) and `logging.py` (thread-safe structured logging).

3. Persistence & Database Layer
   - PostgreSQL database accessed asynchronously via asyncpg.
   - Managed using Alembic for database migrations.
   - Tables: users, auth_providers (for multi-provider auth like GitHub, Google, Email).

4. Container Runtime Layer (`dock`)
   - Interfaces with a custom container engine (`dock` / `dock-minidocker`).
   - Handles `dock build`, `dock run`, `dock ps`, and `dock inspect`.

---

## Database Setup

### 1. PostgreSQL Setup

1. Log into PostgreSQL as the superuser:
   ```bash
   sudo -u postgres psql
   ```

2. Create the database and database user:
   ```sql
   CREATE DATABASE parcel;
   CREATE USER parcel WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE parcel TO parcel;
   ALTER DATABASE parcel OWNER TO parcel;
   ```

3. Exit psql:
   ```sql
   \q
   ```

### 2. Environment Configuration

Copy the example environment file and set your credentials:
```bash
cp backend/.env.example backend/.env
```

Ensure `DATABASE_URL` in `backend/.env` is set correctly:
```env
DATABASE_URL=postgresql+asyncpg://parcel:your_secure_password@localhost:5432/parcel
```

### 3. Alembic Database Migrations

Run database migrations to create the required tables (`users`, `auth_providers`, `alembic_version`):

```bash
# Navigate to backend directory
cd backend

# Run pending migrations
alembic upgrade head
```

If you modify models in `backend/app/models/`, generate a new migration:
```bash
alembic revision --autogenerate -m "describe_your_change"
alembic upgrade head
```

---

## Database Models

- users: Primary user profile table (`id`, `name`, `email`, `created_at`, `updated_at`).
- auth_providers: Stores authentication methods associated with users (`id`, `user_id`, `provider`, `provider_user_id`, `password_hash`, `created_at`). Supports `email`, `github`, and `google` authentication.

---

## Core Infrastructure & Utilities

- **`app/core/security.py`**: Handles secure password hashing and verification using `bcrypt`, along with JWT access token generation and validation using `PyJWT`.
- **`app/core/logging.py`**: Custom thread-safe structured logger (`Logger`, `LogLevel`) with support for multi-level logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `FATAL`), exception tracebacks, terminal output (`stdout`/`stderr`), and daily log file writing to `backend/app/logs/`.

---

## Project Boundaries & v1 Roadmap Checklist

### 1. Authentication & User Management
- [x] GitHub OAuth Integration
- [ ] Multi-Provider Authentication (GitHub, Google, Email/Password)
- [x] Password Hashing & JWT Token Management (`app/core/security.py`)
- [x] User & AuthProvider Database Persistence (SQLAlchemy + PostgreSQL + Alembic)

### 2. Core Infrastructure & Logging
- [x] Custom Thread-Safe Application Logging (`app/core/logging.py`)

### 3. Source Code Ingestion
- [x] GitHub Repository Listing via GitHub API
- [ ] ZIP Tarball Source Upload
- [ ] Source Metadata Storage in DB

### 4. Build File Generation
- [ ] Framework detection & dynamic Dockerfile generation
- [ ] Isolated workspace build directories (`/tmp/parcel-builds/`)
- [ ] Build logs and status storage in DB

### 5. Custom Container Runtime (`dock`)
- [ ] Image Building via `dock build`
- [ ] Container Launching via `dock run`
- [ ] Monitoring via `dock ps` and `dock inspect`
- [ ] Persisting telemetry, ports, and logs to DB

---

## Quick Start Guide

### 1. Start Backend API
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.
