from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.command_history import CommandHistory
from app.utils.enums import Direction


class CommandHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_history(
        self,
        robot_id: int,
        command_string: str,
        initial_x: int,
        initial_y: int,
        initial_direction: Direction,
        final_x: int,
        final_y: int,
        final_direction: Direction,
        stopped_by_obstacle: bool = False,
        obstacle_x: Optional[int] = None,
        obstacle_y: Optional[int] = None,
    ) -> CommandHistory:
        history = CommandHistory(
            robot_id=robot_id,
            command_string=command_string,
            initial_x=initial_x,
            initial_y=initial_y,
            initial_direction=initial_direction.value,
            final_x=final_x,
            final_y=final_y,
            final_direction=final_direction.value,
            stopped_by_obstacle=stopped_by_obstacle,
            obstacle_x=obstacle_x,
            obstacle_y=obstacle_y,
        )
        self.db.add(history)
        await self.db.commit()
        await self.db.refresh(history)
        return history
