from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.models.robot import Robot
from app.utils.enums import Direction


class RobotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_robot(self) -> Optional[Robot]:
        """singleton - one robot exist"""
        result = await self.db.execute(select(Robot).limit(1))
        return result.scalar_one_or_none()

    async def create_robot(self, x: int, y: int, direction: Direction) -> Robot:
        robot = Robot(x=x, y=y, direction=direction.value)
        self.db.add(robot)
        await self.db.commit()
        await self.db.refresh(robot)
        return robot

    async def get_or_create_robot(self) -> Robot:
        robot = await self.get_robot()

        if robot is None:
            settings = get_settings()
            robot = await self.create_robot(
                x=settings.start_position_x,
                y=settings.start_position_y,
                direction=Direction(settings.start_direction),
            )

        return robot

    async def update_position(self, robot: Robot, x: int, y: int, direction: Direction) -> Robot:
        robot.x = x
        robot.y = y
        robot.direction = direction.value
        await self.db.commit()
        await self.db.refresh(robot)
        return robot
