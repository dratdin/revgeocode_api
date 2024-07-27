from enum import Enum
from uuid import UUID
from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel, ConfigDict, model_validator, field_validator
from pydantic_extra_types.coordinate import Longitude, Latitude


class CsvData(BaseModel):
    points: Annotated[list[str], Len(min_length=1)]
    coords: Annotated[list[tuple[Latitude, Longitude]], Len(min_length=1)]

    @field_validator("points", "coords")
    @classmethod
    def valid_unique_items(cls, value: list):
        if len(set(value)) != len(value):
            raise ValueError("Duplicates found")
        return value

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.points) != len(self.coords):
            raise ValueError(
                "Number of points is not the same as coordinates"
            )

        return self


class TaskStatusEnum(str, Enum):
    running = "running"
    done = "done"
    failed = "failed"


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_id: UUID
    status: TaskStatusEnum


class Point(BaseModel):
    name: str
    address: str


class Link(BaseModel):
    name: str
    distance: float


class GetTaskResults(BaseModel):
    task_id: UUID
    status: TaskStatusEnum

    points: list[Point] | None
    links: list[Link] | None
