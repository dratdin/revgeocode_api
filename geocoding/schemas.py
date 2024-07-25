from enum import Enum
from uuid import UUID

from typing import Annotated
from annotated_types import Len
from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.coordinate import Longitude, Latitude

from .constants import POINT, LATITUDE, LONGITUDE


class Location(BaseModel):
    name: str = Field(alias=POINT)
    lat: Latitude = Field(alias=LATITUDE)
    lng: Longitude = Field(alias=LONGITUDE)


class TaskLocations(BaseModel):
    locations: Annotated[list[Location], Len(min_length=1)]


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
