from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.robot_schema import CommandRequest, CommandResponse, PositionResponse
from app.services.robot_service import RobotService

router = APIRouter(prefix="/robot", tags=["robot"])


@router.get("/position", response_model=PositionResponse)
async def get_position(db: AsyncSession = Depends(get_db)) -> PositionResponse:
    """Get current robot position and direction."""
    service = RobotService(db)
    x, y, direction = await service.get_position()

    return PositionResponse(x=x, y=y, direction=direction.value)


@router.post("/commands", response_model=CommandResponse)
async def execute_commands(
    request: CommandRequest, db: AsyncSession = Depends(get_db)
) -> CommandResponse:
    """Execute a string of commands and return final position."""
    service = RobotService(db)
    x, y, direction, stopped_by_obstacle, obstacle_coordinate = await service.execute_commands(
        request.commands
    )

    return CommandResponse(
        x=x,
        y=y,
        direction=direction.value,
        commands_executed=request.commands,
        stopped_by_obstacle=stopped_by_obstacle,
        obstacle_coordinate=obstacle_coordinate,
    )
