# Auto Listings Service

Service for collecting car listings, viewing them in an admin panel, and searching through a Telegram bot.

## Stack

- Backend: FastAPI, SQLAlchemy Async, Alembic, PostgreSQL
- Frontend: React + TypeScript + Vite + Nginx
- Worker: ARQ + Redis queue for periodic listing sync
- Bot: Telegram + OpenAI Function Calling

## Setup & Run

```bash
cp .env.example .env
# Fill in TELEGRAM_BOT_TOKEN and LLM_API_KEY if needed, then:
docker-compose up --build
```

## URLs

- Frontend + API gateway: http://localhost
- Backend health check (through nginx): http://localhost/health

## Authentication

- Username: `admin`
- Password: `admin123`

## API

- `POST /api/login`
- `GET /api/cars` (JWT required, supports `make`, `model`, `color`, `max_price`, `min_year`, `limit`, `offset`)

## Architecture

```
backend/src/
  api/          # Routes and JWT bearer dependency
  services/     # Business logic, no direct DB access
  repositories/ # Database queries via SQLAlchemy async
  adapters/     # External data source adapters (CarSensor); swap without touching services
  core/         # JWT creation/validation, bcrypt password hashing
  tasks/        # ARQ cron job for periodic listing sync with retry/backoff
  fixtures/     # Admin user seeding (runs before server start)
bot/src/
  filter_parser.py  # OpenAI Responses API function-calling; regex fallback if no key
  main.py           # aiogram Telegram dispatcher
frontend/src/   # React SPA, React Query, Axios with JWT interceptor
```

**Key decisions:**

- **FastAPI + async SQLAlchemy** — native async stack avoids thread overhead under I/O-heavy scraping load.
- **Repository pattern** — services depend on protocols, not concrete classes; simplifies unit testing and swapping DB backends.
- **Adapter pattern for scrapers** — `BaseListingsAdapter` lets new sources be added without touching sync logic or services.
- **ARQ + Redis** — lightweight task queue that fits a single-service deployment; cron built-in, no Celery overhead.
- **Upsert by `source_url`** — idempotent sync: re-running never creates duplicates, only updates changed fields.
- **OpenAI Responses API with regex fallback** — bot works without an API key; LLM improves filter extraction when available.
- **Alembic migrations + seed script** — schema versioned from day one; admin account created automatically on first start.

## Notes

- Worker performs batch upsert by unique `source_url`.
- Scraper runs in Redis queue with retries and cron scheduling.
- If `LLM_API_KEY` is not set, the bot uses a fallback regex parser.

## Tests

```bash
cd backend && uv run pytest tests/
```
