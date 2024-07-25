import itertools as it
import pandas as pd

import geopy.distance
from geopy.geocoders import Nominatim

from .schemas import Link, Point, Task
from .models import ModelsRepo

geolocator = Nominatim(user_agent="revgeocode_api_v2")


async def reverse_geocode(task: Task, locs_df: pd.DataFrame):
    try:
        print(f"Executing {task.task_id}")

        # Calc links
        links = []
        for p1, p2 in it.combinations(locs_df.index, 2):
            coords_1 = locs_df.loc[p1]
            coords_2 = locs_df.loc[p2]
            links.append(
                Link(
                    name=p1 + p2, distance=geopy.distance.geodesic(coords_1, coords_2).m
                )
            )

        points = []
        for i, data in locs_df.iterrows():
            points.append(
                Point(name=i, address=geolocator.reverse(data).address)
            )

        await ModelsRepo.complete_task(task.task_id, links, points)
    except Exception:
        await ModelsRepo.fail_task(task.task_id)
        raise
