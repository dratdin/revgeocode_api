import csv
from io import StringIO
import itertools as it

import geopy.distance
from geopy.geocoders import Nominatim
from fastapi import UploadFile, HTTPException

from .constants import POINT, LATITUDE, LONGITUDE
from .schemas import CsvData, Link, Point, Task
from .repository import TaskRepository

geolocator = Nominatim(user_agent="revgeocode_api_v2")


async def validate_csv_file(csv_file: UploadFile) -> dict[str, tuple[float, float]]:
    # Read csv content
    points, coords = [], []
    fcontent = await csv_file.read()
    with StringIO(fcontent.decode("utf-8")) as buff:
        csv_reader = csv.DictReader(buff)
        if csv_reader.fieldnames != [POINT, LATITUDE, LONGITUDE]:
            raise HTTPException(400, "Unknown CSV column names")

        for row in csv_reader:
            points.append(row[POINT])
            coords.append((row[LATITUDE], row[LONGITUDE]))
    # Validate points and coords
    CsvData.model_validate(
        {
            "points": points,
            "coords": coords,
        }
    )
    return {pnt: crds for pnt, crds in zip(points, coords)}


async def reverse_geocode_bg_task(
    task: Task, locations: dict[str, tuple[float, float]]
):
    print(f"Executing {task.task_id}")

    try:
        # Calc links
        links = [
            Link(
                name=p1 + p2,
                distance=geopy.distance.geodesic(locations[p1], locations[p2]).m,
            )
            for p1, p2 in it.combinations(locations.keys(), 2)
        ]
        # Calc points
        points = [
            Point(name=k, address=geolocator.reverse(v).address)
            for k, v in locations.items()
        ]

        await TaskRepository.complete(task.task_id, links, points)
    except Exception:
        # geopy.distance.geodesic.set_ellipsoid
        # geolocator.reverse._call_geocoder
        # may raise errors as Exception(...)
        await TaskRepository.fail(task.task_id)
        raise
