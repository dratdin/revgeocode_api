from fastapi import FastAPI, Request, status

from fastapi.responses import JSONResponse

from pydantic import ValidationError

from .geocoding.router import router as geocoding_router

app = FastAPI()


app.include_router(
    geocoding_router, prefix="/api",
)


@app.get("/")
async def root():
    return {"message": "Welcome to simple geocoding api!"}


@app.exception_handler(ValidationError)
async def value_error_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"errors": repr(exc).split("\n")},
    )
