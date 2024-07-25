from io import StringIO
import pandas as pd

from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks

from .constants import ALIAS_POINT, ALIAS_LATITUDE, ALIAS_LONGITUDE
from .models import TaskRepository
from .schemas import TaskLocations
from .service import reverse_geocode


router = APIRouter(tags=["geocoding"])


@router.post("/calculateDistances", tags=["reverse-geocoding"], status_code=201)
async def calculate_distances(csv_file: UploadFile, bg_tasks: BackgroundTasks):
    if csv_file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Endpoint only accepts CSV files.")

    # File to DataFrame
    fcontent = await csv_file.read()
    with StringIO(fcontent.decode('utf-8')) as buff:
        df = pd.read_csv(buff, delimiter=",")
    
    # Validate structure
    TaskLocations.model_validate({
        "locations": df.to_dict("records")
    })
    # Validate uniqueness of Point names 
    dup_points = df[ALIAS_POINT].duplicated()
    if dup_points.any():
        raise HTTPException(
            status_code=400,
            detail=(
                f"'{ALIAS_POINT}' values must be unique. "
                f"Duplications: {df.loc[dup_points, ALIAS_POINT].unique().tolist()}"
            )
        )
    df.set_index(ALIAS_POINT, inplace=True)
    # Validate uniqueness coordinates (Latitude, Longitude)
    dup_coords = df.duplicated()
    if dup_coords.any():
        raise HTTPException(
            status_code=400,
            detail=(
                f"'({ALIAS_LATITUDE}, {ALIAS_LONGITUDE})' pairs must be unique across the file. "
                f"Duplications: {df.index[dup_coords].tolist()}"
            )
        )
    
    new_task = await TaskRepository.new()
    
    bg_tasks.add_task(reverse_geocode, new_task, df)
    
    return new_task.model_dump()


@router.get("/getResult")
async def get_result():
    return {
        "task_id": "<XXXX>",
        "status": "mocked",
        "data":
        {
            "points": [
                { "name" : "A", "address" : "Some address…"},
                { "name" : "B", "address" : "Some address…"},
                { "name" : "C", "address" : "Some address…"},
            ],
            "links": [
                { "name" : "AB", "distance" : 350.6},
                { "name" : "BC", "distance" : 125.8},
                { "name" : "AC", "distance" : 1024.9}
            ]
        }
    }
