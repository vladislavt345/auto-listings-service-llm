FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

COPY backend/pyproject.toml backend/uv.lock /app/
RUN uv sync --frozen --no-dev

COPY backend /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
