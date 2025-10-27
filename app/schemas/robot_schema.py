from typing import Literal

from pydantic import BaseModel, Field


class PositionResponse(BaseModel):
    x: int = Field(..., description="X cord")
    y: int = Field(..., description="Y cord")
    direction: Literal["NORTH", "SOUTH", "EAST", "WEST"] = Field(..., description="face direction")

    class Config:
        json_schema_extra = {"example": {"x": 4, "y": 2, "direction": "WEST"}}


class CommandRequest(BaseModel):
    commands: str = Field(
        ...,
        description="Command string (F=Forward, B=Backward, L=Left, R=Right)",
        pattern="^[FBLR]+$",
        min_length=1,
    )

    class Config:
        json_schema_extra = {"example": {"commands": "FLFFFRFLB"}}


class CommandResponse(BaseModel):
    x: int = Field(..., description="final X cord")
    y: int = Field(..., description="final Y cord")
    direction: Literal["NORTH", "SOUTH", "EAST", "WEST"] = Field(
        ..., description="final face direction"
    )
    commands_executed: str = Field(..., description="commands executed")
    stopped_by_obstacle: bool = Field(
        default=False, description="if robot stopped because of obstacle"
    )
    obstacle_coordinate: tuple[int, int] | None = Field(
        default=None, description="if hit by obstacle, its cordinates"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "x": 6,
                "y": 4,
                "direction": "NORTH",
                "commands_executed": "FLFFFRFLB",
                "stopped_by_obstacle": False,
                "obstacle_coordinate": None,
            }
        }
