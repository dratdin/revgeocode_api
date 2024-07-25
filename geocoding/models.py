from uuid import UUID, uuid4
from ..database import Model, db_session

from .schemas import TaskStatusEnum, Task
from sqlalchemy.orm import Mapped, mapped_column


class TaskORM(Model):
    __tablename__ = "tasks"
    
    task_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        unique=True,
        default=uuid4
    )
    status: Mapped[str]


class TaskRepository:
    @classmethod
    async def new(cls, status: str = TaskStatusEnum.running.value) -> Task:
        async with db_session() as session:
            task_orm = TaskORM(status=status)
            session.add(task_orm)
            await session.flush()
            await session.commit()
            return Task.model_validate(task_orm)
