from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..database import async_db_session
from .schemas import TaskStatusEnum, Link, Point
from .models import TaskORM, LinkORM, PointORM


class TaskRepository:
    @classmethod
    async def new(cls, status: str = TaskStatusEnum.running.value) -> TaskORM:
        async with async_db_session() as session:
            task_orm = TaskORM(status=status)
            session.add(task_orm)
            await session.flush()
            await session.commit()
            return task_orm

    @classmethod
    async def get_results(cls, task_id: UUID) -> TaskORM:
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
    async def complete(cls, task_id: UUID, links: list[Link], points: list[Point]):
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
    async def fail(cls, task_id: UUID):
        async with async_db_session() as session:
            task_orm = await session.get(TaskORM, task_id)
            setattr(task_orm, "status", TaskStatusEnum.failed.value)
            await session.commit()
