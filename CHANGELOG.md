# Changelog

## 1.0.0 — 2026-07-08

First production-ready release.

### Features

- File upload with optional title; auto-generated name when title is empty
- Async processing pipeline: scan rules, metadata extraction, alert generation
- Scan rules: suspicious extensions, oversized files, PDF MIME mismatch, magic-byte mismatch
- Vue dashboard: file table, stats, alert timeline, upload drawer, confirm dialogs
- Download and delete files; alerts removed on file delete
- API: list/get/upload/delete/download files, list alerts, health and readiness checks
- Interface RU / EN with localized API and scan messages

### Infrastructure

- Modular async monolith: FastAPI, SQLAlchemy async, PostgreSQL, Taskiq + Redis
- Docker Compose with `dev` / `prod` profiles (`mise run dev` / `mise run up`)
- nginx reverse proxy for production UI and API
- structlog logging, request ID middleware, JSON logs in prod
- Alembic migrations, shared file storage volume
- pre-commit hooks and CI pipeline (ruff, mypy, pytest, vue-tsc, Vitest) with ≥85% coverage gate
