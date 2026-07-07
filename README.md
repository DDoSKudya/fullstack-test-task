# File Exchange

Upload, scan and monitor files. Modular async monolith: FastAPI API, Taskiq worker, Vue dashboard, PostgreSQL, Redis.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [mise](https://mise.jdx.dev/getting-started.html)

## Quick start

```bash
mise install
cp .env.dev .env
mise run dev
```

| Mode | URL |
|------|-----|
| Dev UI | http://localhost:3000 |
| Dev API docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |

## Prod-like stack

```bash
mise run up
```

| URL | Purpose |
|-----|---------|
| http://localhost | UI + API via nginx (`/api/v1/...`) |
| http://localhost/health | API health (proxied) |

Prod overrides: `LOG_FORMAT=json`, `DOCS_ENABLED=false`, no uvicorn reload.

## Architecture

```text
Browser
  ├─ dev:  Vite :3000  ──proxy /api──►  FastAPI :8000
  └─ prod: nginx :80   ──/api──────────►  FastAPI :8000
                      └──/─────────────►  Vue static (frontend-prod)

FastAPI ──enqueue──► Redis (Taskiq) ──► Worker ──► PostgreSQL
         └──read/write──► local volume (/data/files)
```

**Flow:** upload → DB row + file on disk → `process_file` task → scan + metadata → alert → UI polls files/alerts.

## Commands

| Command | Description |
|---------|-------------|
| `mise run migrate` | Apply database migrations |
| `mise run dev` | Lint, install hooks, start dev stack |
| `mise run test` | Lint, mypy, pytest, prod frontend build |
| `mise run up` | Prod-like stack with nginx |
| `mise run down` | Stop dev and prod stacks |

## Configuration

Copy `.env.dev` to `.env`. Key variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | asyncpg URL to postgres | API + worker |
| `REDIS_URL` | `redis://redis:6379/0` | Taskiq broker |
| `STORAGE_PATH` | `/data/files` | Uploaded files (shared volume) |
| `MAX_UPLOAD_MB` | `50` | Upload size limit |
| `SCAN_MAX_MB` | `10` | Suspicious if file larger |
| `LOG_FORMAT` | `console` / `json` | structlog renderer |
| `DOCS_ENABLED` | `true` / `false` | OpenAPI `/docs` |
| `UVICORN_RELOAD` | `--reload` / empty | Dev hot reload only |

## Migrations

```bash
mise run migrate
```

Or inside a running stack:

```bash
docker compose exec api uv run alembic upgrade head
```

## Troubleshooting

**Files stay in `processing`**

- Check worker logs: `docker compose logs worker -f`
- Redis must be healthy; worker depends on postgres + redis.

**Upload fails with 413 or connection reset**

- nginx `client_max_body_size` is 50m (see `infra/nginx/nginx.conf`)
- `MAX_UPLOAD_MB` in `.env` must match expectations

**`mise run dev` fails on lint**

- Run `mise run lint` locally; fix ruff/mypy issues before starting compose.

**Prod UI loads but API errors**

- Run `mise run migrate` after `mise run up`
- API requests must use `/api/v1` prefix (set in frontend prod build)

**Port 80 already in use**

- Stop other web servers or change nginx port mapping in `docker-compose.yml`.

## Windows

Use Docker Desktop with WSL2. Run commands from WSL or Git Bash.

## Project layout

```text
backend/src/   API, services, worker, processing rules
frontend/src/  Vue dashboard, api client, i18n
infra/nginx/   Prod reverse proxy
.plan/         Architecture and phase docs (local, gitignored)
```
