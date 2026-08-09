# AI Job Application Agent

A multi-agent system that helps a user find relevant jobs, analyze fit against
their resume, generate tailored application materials, track applications,
and prepare for interviews — built with FastAPI, LangGraph, and a Celery-backed
async task pipeline.

## Status

**Phase 1: Backend architecture** — complete.

This phase establishes the skeleton every later phase builds on: a running
FastAPI app, Postgres + Redis + Celery wired via Docker Compose, layered
architecture (routers → services → repositories → models), and CI running
lint + type-check + tests on every push. No business logic yet — that starts
in Phase 2 (Database) and Phase 3 (Authentication).

## Architecture

```
backend/app/
├── api/v1/          # HTTP layer: routers, request/response wiring only
├── services/        # Business logic — framework-agnostic
├── repositories/     # DB access layer, one per aggregate
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response schemas
├── ai/                # LangGraph agents, RAG, prompts — isolated from web layer
├── workers/           # Celery tasks for slow/unreliable operations
├── core/              # Settings, security, logging, exception handling
└── db/                # Engine, session, declarative base
```

**Why this layering:** services never touch SQLAlchemy directly (they call
the repository layer), so business logic can be unit-tested by mocking a
repository instead of spinning up Postgres. AI logic lives in its own `ai/`
package rather than inside `services/`, since LLM calls have fundamentally
different failure modes (rate limits, cost, non-determinism) than DB calls
and benefit from being independently testable/mockable.

## Running locally

```bash
cp backend/.env.example backend/.env
# edit backend/.env if needed (defaults work out of the box for local dev)

docker compose up --build
```

Then check:

```bash
curl http://localhost:8000/api/v1/health
# {"api": "ok", "database": "ok", "redis": "ok"}
```

Interactive API docs: http://localhost:8000/docs

## Running tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

## Roadmap

| Phase | Scope |
|---|---|
| 1 | Backend architecture ✅ |
| 2 | Database schema + migrations |
| 3 | Authentication (JWT, OAuth) |
| 4 | Resume parsing & storage |
| 5 | AI job matching |
| 6 | Job collection (scraping pipeline) |
| 7 | Resume optimization & cover letter generation |
| 8 | Multi-agent orchestration (LangGraph) |
| 9 | Interview preparation |
| 10 | Application tracker + analytics dashboard |
| 11 | Frontend (React + TypeScript) |
| 12 | Deployment (AWS, Nginx, CI/CD hardening) |

## Tech stack

**Backend:** Python, FastAPI, PostgreSQL, Redis, Celery, SQLAlchemy
**AI:** LangGraph, LangChain, OpenAI API, Sentence Transformers, ChromaDB
**Frontend (Phase 11):** React, TypeScript, Tailwind CSS, shadcn/ui
**Deployment:** Docker, Docker Compose, GitHub Actions, Nginx
