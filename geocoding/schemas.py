from enum import Enum
from uuid import UUID

from typing import Annotated
from annotated_types import Len
from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.coordinate import Longitude, Latitude

from .constants import ALIAS_POINT, ALIAS_LATITUDE, ALIAS_LONGITUDE


class Location(BaseModel):
    name: str = Field(alias=ALIAS_POINT)
    lat: Latitude = Field(alias=ALIAS_LATITUDE)
    lng: Longitude = Field(alias=ALIAS_LONGITUDE)


class TaskLocations(BaseModel):
    locations: Annotated[list[Location], Len(min_length=1)]


class TaskStatusEnum(str, Enum):
    running = 'running'
    done = 'done'
    failed = 'failed'


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


class ResultData(BaseModel):
    points: list[Point]
    links: list[Link]


class GetResult(BaseModel):
    task_id: UUID
    status: TaskStatusEnum
    data: ResultData | None = None
