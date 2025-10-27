import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.robot_service import RobotService
from app.utils.enums import Direction


@pytest.mark.asyncio
async def test_get_initial_position(test_db_session: AsyncSession) -> None:
    """Test getting initial robot position creates robot with defaults."""
    service = RobotService(test_db_session)

    x, y, direction = await service.get_position()

    assert x == 4
    assert y == 2
    assert direction == Direction.WEST


@pytest.mark.asyncio
async def test_execute_forward_command(test_db_session: AsyncSession) -> None:
    """GIVEN: moving forward updates position correctly."""
    service = RobotService(test_db_session)

    # WHEN: (4, 2, WEST)
    # THEN: move west -> (3, 2, WEST)
    x, y, direction, stopped, obstacle = await service.execute_commands("F")

    assert x == 3
    assert y == 2
    assert direction == Direction.WEST
    assert stopped is False
    assert obstacle is None


@pytest.mark.asyncio
async def test_execute_backward_command(test_db_session: AsyncSession) -> None:
    """GIVEN: moving backward updates position correctly."""
    service = RobotService(test_db_session)

    # WHEN: (4, 2, WEST)
    # THEN: move east -> (5, 2, WEST)
    x, y, direction, stopped, obstacle = await service.execute_commands("B")

    assert x == 5
    assert y == 2
    assert direction == Direction.WEST
    assert stopped is False
    assert obstacle is None


@pytest.mark.asyncio
async def test_execute_turn_left_command(test_db_session: AsyncSession) -> None:
    """GIVE: Test turning left updates direction correctly."""
    service = RobotService(test_db_session)

    # WHEN: (4, 2, WEST)
    # THEN: turn south
    x, y, direction, stopped, obstacle = await service.execute_commands("L")

    assert x == 4
    assert y == 2
    assert direction == Direction.SOUTH
    assert stopped is False
    assert obstacle is None


@pytest.mark.asyncio
async def test_execute_turn_right_command(test_db_session: AsyncSession) -> None:
    """GIVEN: Test turning right updates direction correctly."""
    service = RobotService(test_db_session)

    # WHEN: (4, 2, WEST)
    # THEN: turn north
    x, y, direction, stopped, obstacle = await service.execute_commands("R")

    assert x == 4
    assert y == 2
    assert direction == Direction.NORTH
    assert stopped is False
    assert obstacle is None


@pytest.mark.asyncio
async def test_execute_complex_command_string(test_db_session: AsyncSession) -> None:
    """GIVEN: Test executing multiple commands in sequence."""
    service = RobotService(test_db_session)

    # WHEN: (4, 2, WEST)
    # THEN
    # F: (3, 2, WEST)
    # L: (3, 2, SOUTH)
    # F: (3, 1, SOUTH)
    # F: (3, 0, SOUTH)
    # F: (3, -1, SOUTH)
    # R: (3, -1, WEST)
    # F: (2, -1, WEST)
    # L: (2, -1, SOUTH)
    # B: (2, 0, SOUTH)
    x, y, direction, stopped, obstacle = await service.execute_commands("FLFFFRFLB")

    assert x == 2
    assert y == 0
    assert direction == Direction.SOUTH
    assert stopped is False
    assert obstacle is None


@pytest.mark.asyncio
async def test_execute_maintains_state_between_calls(test_db_session: AsyncSession) -> None:
    """GIVEN: Test that position persists between command executions."""
    service = RobotService(test_db_session)
    # WHEN:
    # 1. move forward
    await service.execute_commands("F")

    # 2. should start from previous position
    x, y, direction, stopped, obstacle = await service.execute_commands("F")

    # THEN: 2 steps west from start: (4, 2) -> (3, 2) -> (2, 2)
    assert x == 2
    assert y == 2
    assert direction == Direction.WEST
    assert stopped is False
    assert obstacle is None


@pytest.mark.asyncio
async def test_execute_only_rotations(test_db_session: AsyncSession) -> None:
    """GIVEN: Test executing only rotation commands doesn't change position."""
    service = RobotService(test_db_session)

    # WHEN: Only turns, no movement
    x, y, direction, stopped, obstacle = await service.execute_commands("RRLL")

    # THEN: Back to original direction
    assert x == 4
    assert y == 2
    assert direction == Direction.WEST
    assert stopped is False
    assert obstacle is None
