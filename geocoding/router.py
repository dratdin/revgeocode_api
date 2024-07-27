from uuid import UUID

from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks

from .repository import TaskRepository
from .schemas import Task, GetTaskResults
from .service import validate_csv_file, reverse_geocode_bg_task


router = APIRouter(tags=["reverse-geocoding"])


@router.post("/calculateDistances", status_code=201, response_model=Task)
async def calculate_distances(csv_file: UploadFile, bg_tasks: BackgroundTasks):
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    locations = await validate_csv_file(csv_file)

    n_task = await TaskRepository.new()

    bg_tasks.add_task(reverse_geocode_bg_task, n_task, locations)

    return n_task


@router.get("/getResult/{task_id}/", response_model=GetTaskResults)
async def get_result(task_id: UUID):
    task_orm = await TaskRepository.get_results(task_id)
    if task_orm is not None:
        return task_orm

    raise HTTPException(status_code=404)
