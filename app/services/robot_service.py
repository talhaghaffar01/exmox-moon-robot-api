from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.command_history_repository import CommandHistoryRepository
from app.repositories.obstacle_repository import ObstacleRepository
from app.repositories.robot_repository import RobotRepository
from app.utils.enums import Direction


class RobotService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.robot_repo = RobotRepository(db)
        self.history_repo = CommandHistoryRepository(db)
        self.obstacle_repo = ObstacleRepository(db)

    async def get_position(self) -> tuple[int, int, Direction]:
        """Get current robot position."""
        robot = await self.robot_repo.get_or_create_robot()
        return robot.x, robot.y, Direction(robot.direction)

    async def execute_commands(
        self, commands: str
    ) -> tuple[int, int, Direction, bool, Optional[tuple[int, int]]]:
        """
        Execute a string of commands and return final position.

        Commands:
        - F: Move forward
        - B: Move backward
        - L: Turn left
        - R: Turn right

        Returns:
            Tuple of (x, y, direction, stopped_by_obstacle, obstacle_coordinate)
        """
        robot = await self.robot_repo.get_or_create_robot()

        # get all obstacles
        obstacles = await self.obstacle_repo.get_obstacle_coordinates()

        # initial state
        initial_x, initial_y = robot.x, robot.y
        initial_direction = Direction(robot.direction)

        # current state
        x, y = robot.x, robot.y
        direction = Direction(robot.direction)

        # if hit an obstacle
        stopped_by_obstacle = False
        obstacle_coordinate: Optional[tuple[int, int]] = None

        # process commands 1 by 1
        for command in commands:
            if command == "F":
                # new position (forward)
                dx, dy = direction.get_delta()
                new_x, new_y = x + dx, y + dy

                # check obstacle
                if (new_x, new_y) in obstacles:
                    stopped_by_obstacle = True
                    obstacle_coordinate = (new_x, new_y)
                    break

                x, y = new_x, new_y

            elif command == "B":
                # new position (backward)
                dx, dy = direction.get_delta()
                new_x, new_y = x - dx, y - dy

                # check obstacle
                if (new_x, new_y) in obstacles:
                    stopped_by_obstacle = True
                    obstacle_coordinate = (new_x, new_y)
                    break

                x, y = new_x, new_y

            elif command == "L":
                direction = direction.turn_left()
            elif command == "R":
                direction = direction.turn_right()

        # update position
        await self.robot_repo.update_position(robot, x, y, direction)

        # save command history
        await self.history_repo.create_history(
            robot_id=robot.id,
            command_string=commands,
            initial_x=initial_x,
            initial_y=initial_y,
            initial_direction=initial_direction,
            final_x=x,
            final_y=y,
            final_direction=direction,
            stopped_by_obstacle=stopped_by_obstacle,
            obstacle_x=obstacle_coordinate[0] if obstacle_coordinate else None,
            obstacle_y=obstacle_coordinate[1] if obstacle_coordinate else None,
        )

        return x, y, direction, stopped_by_obstacle, obstacle_coordinate
