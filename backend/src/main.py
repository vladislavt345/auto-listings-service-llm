"""FastAPI application entrypoint."""

from fastapi import FastAPI

from src.api.routes.auth import router as auth_router
from src.api.routes.cars import router as cars_router
from src.config.logger import setup_logging
from src.constants import ROUTE_HEALTH

setup_logging()

app = FastAPI(title="Auto Listings Service")
app.include_router(auth_router)
app.include_router(cars_router)


@app.get(ROUTE_HEALTH)
def healthcheck() -> dict[str, str]:
    """Return service health status.

    Returns:
        Health status payload.
    """

    return {"status": "ok"}
