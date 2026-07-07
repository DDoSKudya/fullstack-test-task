# File Exchange

Refactored file-exchange service: upload, scan, metadata extraction, alerts.

Stack: FastAPI backend, Vue 3 frontend, Taskiq worker, PostgreSQL, Redis.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [mise](https://mise.jdx.dev/getting-started.html)

## Quick start

```bash
mise install
cp .env.dev .env
mise run dev
```

- API: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Health: http://localhost:8000/health

## Commands

| Command | Description |
|---------|-------------|
| `mise run migrate` | Apply database migrations |
| `mise run dev` | Install hooks, lint and start dev stack |
| `mise run lint` | Sync deps + pre-commit (ruff) |
| `mise run test` | Lint + mypy + pytest in Docker |
| `mise run up` | Prod-like stack with nginx |
| `mise run down` | Stop all stacks |

## Migrations

```bash
mise run migrate
```

Or manually:

```bash
docker compose exec api uv run alembic upgrade head
```

## Windows

Use Docker Desktop with WSL2 backend. Run commands from WSL or Git Bash.
