from fastapi import APIRouter, Depends
from app.schemas.health import HealthResponse
from app.services.health_service import get_health_status
from app.core.dependencies import get_application_name


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    return get_health_status()

@router.get("/info")
def info(
    name=Depends(get_application_name)
):

    return {
        "application":name
    }