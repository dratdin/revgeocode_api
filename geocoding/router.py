from uuid import UUID
from io import StringIO
import pandas as pd
from typing import Any

from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks

from .constants import POINT, LATITUDE, LONGITUDE
from .models import ModelsRepo
from .schemas import TaskLocations, GetTaskResults
from .service import reverse_geocode


router = APIRouter(tags=["reverse-geocoding"])


@router.post("/calculateDistances", status_code=201)
async def calculate_distances(csv_file: UploadFile, bg_tasks: BackgroundTasks):
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV allowed")

    # File to DataFrame
    fcontent = await csv_file.read()
    with StringIO(fcontent.decode("utf-8")) as buff:
        df = pd.read_csv(buff, delimiter=",")

    # Validate structure
    TaskLocations.model_validate({"locations": df.to_dict("records")})
    # Validate uniqueness of Point names
    dup_points = df[POINT].duplicated()
    if dup_points.any():
        raise HTTPException(
            status_code=400,
            detail=(
                f"'{POINT}' values must be unique. "
                f"Duplications: {df.loc[dup_points, POINT].unique().tolist()}"
            ),
        )
    df.set_index(POINT, inplace=True)
    # Validate uniqueness coordinates (Latitude, Longitude)
    dup_coords = df.duplicated()
    if dup_coords.any():
        raise HTTPException(
            status_code=400,
            detail=(
                f"'({LATITUDE}, {LONGITUDE})' pairs must be unique. "
                f"Duplications: {df.index[dup_coords].tolist()}"
            ),
        )

    n_task = await ModelsRepo.new_task()
    # Run background task
    bg_tasks.add_task(reverse_geocode, n_task, df)
    return n_task.model_dump()


@router.get("/getResult/{task_id}/", response_model=GetTaskResults)
async def get_result(task_id: UUID):
    task_orm = await ModelsRepo.get_task_results(task_id)
    if task_orm is not None:
        return task_orm

    raise HTTPException(status_code=404)
