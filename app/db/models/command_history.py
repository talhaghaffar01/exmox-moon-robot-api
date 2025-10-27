from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class CommandHistory(Base, TimestampMixin):
    __tablename__ = "command_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    robot_id: Mapped[int] = mapped_column(Integer, ForeignKey("robots.id"), nullable=False)
    command_string: Mapped[str] = mapped_column(Text, nullable=False)
    initial_x: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_y: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_direction: Mapped[str] = mapped_column(String(10), nullable=False)
    final_x: Mapped[int] = mapped_column(Integer, nullable=False)
    final_y: Mapped[int] = mapped_column(Integer, nullable=False)
    final_direction: Mapped[str] = mapped_column(String(10), nullable=False)
    stopped_by_obstacle: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    obstacle_x: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    obstacle_y: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<CommandHistory(id={self.id}, robot_id={self.robot_id}, command='{self.command_string}')>"
