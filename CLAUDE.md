# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LiTR is an AI-powered TRPG (Tabletop Role-Playing Game) web platform with a Python/FastAPI backend and Next.js frontend. An AI Game Master (Google Gemini 2.5 Flash) runs TRPG sessions, with features including dice rolling, character/scenario management, multiplayer, voice chat, and social features. The primary language for code comments and UI is Korean.

## Build & Run Commands

### Backend (project root)
```bash
pip install -r requirements.txt
alembic upgrade head                    # run database migrations
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (`litr-frontend/`)
```bash
npm install                             # also runs prisma generate via postinstall
npm run dev                             # development server (uses --webpack flag)
npm run build                           # production build
npm run lint                            # ESLint
```

### Testing
```bash
# Backend (from root) - uses SQLite test DB, no external services needed
python -m pytest --tb=short -q
# CI also installs: pip install pytest pytest-cov httpx

# Frontend
npm run test:coverage
npm run typecheck
```

### Required Environment Variables
- Backend `.env`: `DATABASE_URL`, `GOOGLE_AI_API_KEY`, `JWT_SECRET_KEY`, `FRONTEND_URL`, `ALLOWED_ORIGINS`
- Frontend `.env.local`: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SOCKET_URL`
- Tests auto-set: `DATABASE_URL=sqlite:///./test.db`, `JWT_SECRET_KEY=test-secret-key`

## Architecture

### Backend (FastAPI, Python 3.11)
- **`main.py`** — App entry point. Registers all routers, middleware stack, and seeds preset scenarios on startup.
- **`database.py`** — SQLAlchemy engine/session setup with PostgreSQL (Supabase). `get_db()` is the FastAPI dependency for DB sessions. Includes auto-migration for missing columns.
- **`routers/`** — 17 route modules. `chat.py` (~79KB) is the core AI GM logic. Each router is a self-contained FastAPI `APIRouter`.
- **`models/`** — SQLAlchemy ORM models: `user`, `game_session`, `character`, `scenario`, `friendship`, `notification`, `analytics`, `transaction`. All inherit from `database.Base`.
- **`schemas/`** — Pydantic request/response models (`auth.py`, `gameplay.py`).
- **`middleware/`** — Security headers, input sanitization, SQL injection protection, CSRF, rate limiting (slowapi).
- **`utils/`** — JWT handling, OAuth helpers, Redis client, logging, friend tag generation.
- **`alembic/`** — Database migration scripts. Config in `alembic.ini`.

### Frontend (Next.js 16, React 19, TypeScript)
- Uses **App Router** (`src/app/`). Pages: home, auth callback, privacy, terms.
- **`src/app/api/`** — Next.js API routes that proxy to the FastAPI backend.
- **State**: Redux Toolkit + Redux Persist for global state, TanStack React Query for server data.
- **`src/middleware.ts`** — Security headers middleware (X-Frame-Options, XSS protection).
- **Prisma ORM** — `prisma/schema.prisma` mirrors the backend DB schema for frontend API routes.
- **i18n** — `messages/en.json` and `messages/ko.json` for English/Korean.
- **3D Dice** — Three.js + Cannon.js physics engine at `public/dice/`.
- Output mode: `standalone` (for Railway Docker deployment).

### Key Patterns
- **Dependency injection**: FastAPI's `Depends()` for DB sessions (`get_db`) and auth (`get_current_user`).
- **Dual game state storage**: JSON files (`routers/game.py`) and database (`routers/game_db.py`).
- **Test fixtures**: `conftest.py` provides `db_session`, `client`, `test_user`, `auth_headers` fixtures using SQLite.
- **Middleware pipeline order** (in `main.py`): SecurityHeaders → InputSanitization → SQLInjectionProtection → CSRF → RateLimit → CORS.

### External Services
- **Supabase** — PostgreSQL database + file storage
- **Google Gemini** — AI Game Master (`google-genai`)
- **OpenAI** — DALL-E 3 image generation (optional)
- **Agora** — Voice chat (optional)
- **Redis** — Caching and rate limiting (optional)

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on push to `main`/`develop` and PRs to `main`:
- Frontend job: lint → typecheck → test:coverage → build
- Backend job: install deps → pytest
- Deployment target: Railway (Docker)
