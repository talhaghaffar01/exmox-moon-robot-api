import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_position_initial(client: AsyncClient) -> None:
    """GIVEN: Test getting initial robot position."""

    # WHEN:
    response = await client.get("/api/v1/robot/position")

    # THEN:
    assert response.status_code == 200
    data = response.json()

    assert data["x"] == 4
    assert data["y"] == 2
    assert data["direction"] == "WEST"


@pytest.mark.asyncio
async def test_execute_commands_forward(client: AsyncClient) -> None:
    """GIVEN: Test executing forward command."""

    # WHEN
    response = await client.post("/api/v1/robot/commands", json={"commands": "F"})

    # THEN
    assert response.status_code == 200
    data = response.json()

    assert data["x"] == 3
    assert data["y"] == 2
    assert data["direction"] == "WEST"
    assert data["commands_executed"] == "F"


@pytest.mark.asyncio
async def test_execute_commands_complex(client: AsyncClient) -> None:
    """GIVEN: Test executing complex command string."""

    # WHEN
    response = await client.post("/api/v1/robot/commands", json={"commands": "FLFFFRFLB"})

    # THEN
    assert response.status_code == 200
    data = response.json()

    assert "x" in data
    assert "y" in data
    assert "direction" in data
    assert data["commands_executed"] == "FLFFFRFLB"


@pytest.mark.asyncio
async def test_execute_commands_invalid_characters(client: AsyncClient) -> None:
    """GIVEN: Test that invalid command characters are rejected."""

    # WHEN:
    response = await client.post("/api/v1/robot/commands", json={"commands": "FXYZ"})

    # THEN: Validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_execute_commands_empty_string(client: AsyncClient) -> None:
    """GIVEN: Test that empty command string is rejected."""

    # WHEN:
    response = await client.post("/api/v1/robot/commands", json={"commands": ""})

    # THEN: # Validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_position_persists_after_commands(client: AsyncClient) -> None:
    """GIVEN: Test that position persists after executing commands."""

    # WHEN:
    # 1
    await client.post("/api/v1/robot/commands", json={"commands": "FF"})

    # 2
    response = await client.get("/api/v1/robot/position")
    data = response.json()

    # THEN: Should be 2 steps west: (4, 2) -> (2, 2)
    assert data["x"] == 2
    assert data["y"] == 2


@pytest.mark.asyncio
async def test_execute_all_command_types(client: AsyncClient) -> None:
    """GIVEN: Test that all command types (F, B, L, R) work."""

    # WHEN:
    response = await client.post("/api/v1/robot/commands", json={"commands": "FBLR"})

    # THEN: Should have valid response structure

    assert response.status_code == 200
    data = response.json()
    assert "x" in data
    assert "y" in data
    assert "direction" in data
