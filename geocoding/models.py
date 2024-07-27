from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Model


class TaskORM(Model):
    __tablename__ = "tasks"

    task_id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, default=uuid4)
    status: Mapped[str]

    links: Mapped[list["LinkORM"]] = relationship(back_populates="task")
    points: Mapped[list["PointORM"]] = relationship(back_populates="task")


class LinkORM(Model):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=False)
    distance: Mapped[float]

    task_id: Mapped[UUID] = mapped_column(ForeignKey(TaskORM.task_id))
    task: Mapped["TaskORM"] = relationship(back_populates="links")


class PointORM(Model):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=False)
    address: Mapped[str] = mapped_column(String(500), unique=False)

    task_id: Mapped[UUID] = mapped_column(ForeignKey(TaskORM.task_id))
    task: Mapped["TaskORM"] = relationship(back_populates="points")
