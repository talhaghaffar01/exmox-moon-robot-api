from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging_config import get_logger
from app.repositories.obstacle_repository import ObstacleRepository

logger = get_logger(__name__)


async def initialize_obstacles(db: AsyncSession) -> None:
    """initialise obstacles from env"""
    settings = get_settings()
    obstacle_repo = ObstacleRepository(db)

    obstacle_coords = settings.parse_obstacles()

    if not obstacle_coords:
        logger.info("No obstacles configured")
        return

    existing = await obstacle_repo.get_obstacle_coordinates()

    # create new obstacles ONLY
    new_obstacles = obstacle_coords - existing

    if new_obstacles:
        await obstacle_repo.bulk_create_obstacles(new_obstacles)
        logger.info(f"Initialized {len(new_obstacles)} obstacles: {new_obstacles}")
    else:
        logger.info(f"Obstacles already initialized: {existing}")
