# Auto Listings Service

Service for collecting car listings, viewing them in an admin panel, and searching through a Telegram bot.

## Stack

- Backend: FastAPI, SQLAlchemy Async, Alembic, PostgreSQL
- Frontend: React + TypeScript + Vite + Nginx
- Worker: ARQ + Redis queue for periodic listing sync
- Bot: Telegram + OpenAI Function Calling

## Run

```bash
cp .env.example .env
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

- `backend/src/api`: routes and dependencies
- `backend/src/services`: business logic only
- `backend/src/clients`: external API clients
- `backend/src/core`: security/core utilities
- `backend/src/fixtures`: seed data scripts
- `backend/src/repositories`: database access
- `backend/src/tasks`: ARQ jobs and worker config
- `bot/src`: Telegram bot + LLM parser (separate service)
- `frontend/src`: SPA

## Notes

- Worker performs batch upsert by unique `source_url`.
- Scraper runs in Redis queue with retries and cron scheduling.
- If `LLM_API_KEY` is not set, the bot uses a fallback regex parser.

## Tests

```bash
pip install -r backend/requirements-dev.txt
pytest backend/tests
```
