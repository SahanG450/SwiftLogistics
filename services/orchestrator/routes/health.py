"""Health check endpoint."""

from fastapi import APIRouter
from datetime import datetime
import sys

sys.path.append('/app')
from common.models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="orchestrator",
        timestamp=datetime.utcnow()
    )
