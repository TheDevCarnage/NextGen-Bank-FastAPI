from fastapi import APIRouter
from backend.app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/home")


@router.get("/ping")
async def health_check():
    return "pong"
