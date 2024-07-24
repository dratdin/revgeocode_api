from enum import Enum

from typing import Annotated
from annotated_types import Len
from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Longitude, Latitude

from .constants import ALIAS_POINT, ALIAS_LATITUDE, ALIAS_LONGITUDE


class Location(BaseModel):
    name: str = Field(alias=ALIAS_POINT)
    lat: Latitude = Field(alias=ALIAS_LATITUDE)
    lng: Longitude = Field(alias=ALIAS_LONGITUDE)


class CalculateDistances(BaseModel):
    locations: Annotated[list[Location], Len(min_length=1)]


class TaskStatusEnum(str, Enum):
    running = 'running'
    done = 'done'
    failed = 'failed'


class Task(BaseModel):
    task_id: str
    status: TaskStatusEnum = TaskStatusEnum.running


class Point(BaseModel):
    name: str
    address: str


class Link(BaseModel):
    name: str
    distance: float


class TaskResultData(BaseModel):
    points: list[Point]
    links: list[Link]


class TaskResult(BaseModel):
    task_id: str
    status: TaskStatusEnum = TaskStatusEnum.running
    data: TaskResultData | None = None
