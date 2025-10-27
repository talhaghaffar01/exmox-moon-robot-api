from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Obstacle(Base, TimestampMixin):
    __tablename__ = "obstacles"
    __table_args__ = (UniqueConstraint("x", "y", name="uq_obstacle_coordinates"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Obstacle(id={self.id}, x={self.x}, y={self.y})>"
