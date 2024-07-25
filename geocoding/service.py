import itertools as it
import pandas as pd

import geopy.distance
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="revgeocode_api")


from .constants import ALIAS_ADDRESS
from .schemas import Task


def reverse_geocode(task: Task, locs_df: pd.DataFrame):
    print(f"Executing {task.task_id}")
    
    # Calc links
    links = {}
    for p1, p2 in it.combinations(locs_df.index, 2):
        coords_1 = locs_df.loc[p1]
        coords_2 = locs_df.loc[p2]
        links[p1 + p2] = geopy.distance.geodesic(coords_1, coords_2).m
    print(f"Links: {links}")
    
    locs_df[ALIAS_ADDRESS] = locs_df.apply(lambda row: geolocator.reverse(tuple(row)).address, axis=1)

    print(f"Addresses")
    print(locs_df[ALIAS_ADDRESS])
