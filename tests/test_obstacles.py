import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.obstacle_repository import ObstacleRepository
from app.services.robot_service import RobotService


@pytest.mark.asyncio
async def test_robot_stops_before_obstacle(test_db_session: AsyncSession) -> None:
    """GIVEN:robot stops before hitting an obstacle."""

    # WHEN: Create obstacle at (3, 2)
    obstacle_repo = ObstacleRepository(test_db_session)
    await obstacle_repo.create_obstacle(3, 2)

    # THEN: Robot starts at (4, 2, WEST), F would move to (3, 2) but there's an obstacle.
    # Robot should stay at (4, 2)

    service = RobotService(test_db_session)
    x, y, direction, stopped, obstacle_coord = await service.execute_commands("F")

    assert x == 4
    assert y == 2
    assert stopped is True
    assert obstacle_coord == (3, 2)


@pytest.mark.asyncio
async def test_robot_stops_mid_command_string(test_db_session: AsyncSession) -> None:
    """GIVEN: robot stops mid-command when hitting obstacle."""

    # WHEN: Create obstacle at (3, 1)
    obstacle_repo = ObstacleRepository(test_db_session)
    await obstacle_repo.create_obstacle(3, 1)

    # Robot at (4, 2, WEST)
    # F -> (3, 2)
    # L -> (3, 2, SOUTH)
    # F -> (3, 1)
    # OBSTACLE..!
    service = RobotService(test_db_session)
    x, y, direction, stopped, obstacle_coord = await service.execute_commands("FLF")

    # THEN: Should stop at (3, 2, SOUTH)
    assert x == 3
    assert y == 2
    assert direction.value == "SOUTH"
    assert stopped is True
    assert obstacle_coord == (3, 1)


@pytest.mark.asyncio
async def test_robot_continues_without_obstacles(test_db_session: AsyncSession) -> None:
    """GIVEN: robot moves normally when no obstacles in path."""
    # WHEN: No obstacles created
    service = RobotService(test_db_session)
    x, y, direction, stopped, obstacle_coord = await service.execute_commands("FFFF")

    # THEN: Should move 4 steps west
    assert x == 0
    assert y == 2
    assert stopped is False
    assert obstacle_coord is None


@pytest.mark.asyncio
async def test_backward_movement_detects_obstacle(test_db_session: AsyncSession) -> None:
    """GIVEN: backward movement also detects obstacles."""

    # WHEN:
    # Create obstacle at (5, 2)
    obstacle_repo = ObstacleRepository(test_db_session)
    await obstacle_repo.create_obstacle(5, 2)

    # THEN: Robot at (4, 2, WEST), B would move backward (east) to (5, 2) but obstacle!

    service = RobotService(test_db_session)
    x, y, direction, stopped, obstacle_coord = await service.execute_commands("B")

    # Should stay at (4, 2)
    assert x == 4
    assert y == 2
    assert stopped is True
    assert obstacle_coord == (5, 2)


@pytest.mark.asyncio
async def test_multiple_obstacles(test_db_session: AsyncSession) -> None:
    """GIVEN: robot navigation with multiple obstacles."""

    # WHEN:
    # Create obstacles
    obstacle_repo = ObstacleRepository(test_db_session)
    await obstacle_repo.bulk_create_obstacles({(1, 4), (3, 5), (7, 4)})

    # Robot at (4, 2, WEST)
    # Execute commands
    service = RobotService(test_db_session)
    x, y, direction, stopped, obstacle_coord = await service.execute_commands("RFF")

    # THEN:Should be at (4, 4, NORTH) , no obstacle
    assert x == 4
    assert y == 4
    assert stopped is False
    assert obstacle_coord is None


@pytest.mark.asyncio
async def test_rotation_does_not_trigger_obstacle(test_db_session: AsyncSession) -> None:
    """GIVEN: rotation commands not trigger obstacle detector."""

    # WHEN:
    # Create obstacle at (3, 2)
    obstacle_repo = ObstacleRepository(test_db_session)
    await obstacle_repo.create_obstacle(3, 2)

    # Robot at (4, 2, WEST)
    service = RobotService(test_db_session)
    x, y, direction, stopped, obstacle_coord = await service.execute_commands("LLLL")

    # THEN: Should still be at (4, 2), face west
    assert x == 4
    assert y == 2
    assert direction.value == "WEST"
    assert stopped is False
    assert obstacle_coord is None
