FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/backend:/app

COPY bot/pyproject.toml bot/uv.lock /app/
RUN uv sync --frozen

COPY bot /app/bot
COPY backend /app/backend

CMD ["python", "-m", "bot.src.main"]
