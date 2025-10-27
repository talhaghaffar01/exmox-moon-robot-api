from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.obstacle import Obstacle


class ObstacleRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_obstacles(self) -> list[Obstacle]:
        result = await self.db.execute(select(Obstacle))
        return list(result.scalars().all())

    async def get_obstacle_coordinates(self) -> set[tuple[int, int]]:
        obstacles = await self.get_all_obstacles()
        return {(obs.x, obs.y) for obs in obstacles}

    async def is_obstacle_at(self, x: int, y: int) -> bool:
        result = await self.db.execute(select(Obstacle).where(Obstacle.x == x, Obstacle.y == y))
        return result.scalar_one_or_none() is not None

    async def create_obstacle(self, x: int, y: int) -> Obstacle:
        obstacle = Obstacle(x=x, y=y)
        self.db.add(obstacle)
        await self.db.commit()
        await self.db.refresh(obstacle)
        return obstacle

    async def bulk_create_obstacles(self, coordinates: set[tuple[int, int]]) -> list[Obstacle]:
        obstacles = [Obstacle(x=x, y=y) for x, y in coordinates]
        self.db.add_all(obstacles)
        await self.db.commit()
        return obstacles
