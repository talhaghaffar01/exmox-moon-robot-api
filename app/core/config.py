from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings loaded from env varibles."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Literal["development", "production", "test"] = "development"
    debug: bool = True
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://robot:robot_password@localhost:5432/moon_robot",
        description="connection str",
    )

    # robot initial config
    start_position_x: int = Field(default=4, description="initial x cord")
    start_position_y: int = Field(default=2, description="initial y cord")
    start_direction: Literal["NORTH", "SOUTH", "EAST", "WEST"] = Field(
        default="WEST", description="initial face direction"
    )

    # obsctles
    obstacles: str = Field(
        default="1,4;3,5;7,4",
        description="list of obstactles cords",
    )

    @field_validator("obstacles")
    @classmethod
    def validate_obstacles(cls, v: str) -> str:
        if not v:
            return v

        try:
            for obstacle in v.split(";"):
                obstacle = obstacle.strip()
                if not obstacle:
                    continue
                parts = obstacle.split(",")
                if len(parts) != 2:
                    raise ValueError(f"Invalid format: {obstacle}")
                int(parts[0]), int(parts[1])
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid obstacles format. Expected 'x,y;x,y' format: {e}")

        return v

    def parse_obstacles(self) -> set[tuple[int, int]]:
        if not self.obstacles:
            return set()

        obstacles_set = set()
        for obstacle in self.obstacles.split(";"):
            obstacle = obstacle.strip()
            if not obstacle:
                continue
            x, y = map(int, obstacle.split(","))
            obstacles_set.add((x, y))

        return obstacles_set

    @property
    def database_url_str(self) -> str:
        return str(self.database_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
