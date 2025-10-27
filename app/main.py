from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import health, robot
from app.core.config import get_settings
from app.core.logging_config import get_logger, setup_logging
from app.db.session import AsyncSessionLocal, close_db
from app.services.obstacle_service import initialize_obstacles

setup_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("starting application...")
    logger.info(f"Env: {settings.environment}")
    logger.info(f"initial position: ({settings.start_position_x}, {settings.start_position_y})")
    logger.info(f"initial direction: {settings.start_direction}")
    logger.info(f"obscatles: {settings.obstacles}")

    async with AsyncSessionLocal() as db:
        await initialize_obstacles(db)

    yield

    logger.info("Shutting down Moon Robot API...")
    await close_db()


# create app
app = FastAPI(
    title="Moon Robot Control API",
    description="fastapi project for moon-robot-api",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(robot.router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    return {
        "message": "Moon Robot Control API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
