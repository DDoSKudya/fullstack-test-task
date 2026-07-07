# File Exchange

Refactored file-exchange service: upload, scan, metadata extraction, alerts.

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
| `mise run dev` | Lint + start dev stack |
| `mise run lint` | Pre-commit, ruff, mypy |
| `mise run test` | Lint + pytest |
| `mise run up` | Prod-like stack with nginx |
| `mise run down` | Stop all stacks |

## Migrations

```bash
docker compose -f docker-compose.dev.yml exec api uv run alembic upgrade head
```

## Windows

Use Docker Desktop with WSL2 backend. Run commands from WSL or Git Bash.
