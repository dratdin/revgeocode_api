from uuid import UUID, uuid4
from ..database import Model, async_db_session

from .schemas import Task, TaskStatusEnum, Link, Point
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload


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


class ModelsRepo:
    @classmethod
    async def new_task(cls, status: str = TaskStatusEnum.running.value) -> Task:
        async with async_db_session() as session:
            task_orm = TaskORM(status=status)
            session.add(task_orm)
            await session.flush()
            await session.commit()
            return Task.model_validate(task_orm)

    @classmethod
    async def get_task_results(cls, task_id: UUID) -> TaskORM:
        async with async_db_session() as session:
            return (
                await session.scalars(
                    select(TaskORM)
                    .where(TaskORM.task_id == task_id)
                    .options(
                        joinedload(TaskORM.links),
                        joinedload(TaskORM.points),
                    )
                )
            ).first()

    @classmethod
    async def complete_task(cls, task_id: UUID, links: list[Link], points: list[Point]):
        async with async_db_session() as session:
            task_orm = await session.get(TaskORM, task_id)
            session.add_all(
                [LinkORM(task_id=task_id, **lnk.model_dump()) for lnk in links]
            )
            session.add_all(
                [PointORM(task_id=task_id, **pt.model_dump()) for pt in points]
            )
            setattr(task_orm, "status", TaskStatusEnum.done.value)
            await session.commit()

    @classmethod
    async def fail_task(cls, task_id: UUID):
        async with async_db_session() as session:
            task_orm = await session.get(TaskORM, task_id)
            setattr(task_orm, "status", TaskStatusEnum.failed.value)
            await session.commit()
