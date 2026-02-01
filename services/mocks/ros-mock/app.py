from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.settings import settings
from src.routes.ros_routes import router as ros_router
from src.routes.manifest_routes import router as manifest_router
from src.services.manifest_service import ManifestService

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Route Optimization System Mock Service for Swift Logistics - Modern cloud-based RESTful API",
    version="2.0.0",
    redoc_url=None,  # Disable ReDoc, use Swagger UI only
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ros_router)
app.include_router(manifest_router)


@app.get("/")
async def root():
    """Root endpoint - ROS Service Information"""
    return {
        "service": settings.app_name,
        "description": "Route Optimization System - Modern cloud-based third-party service",
        "status": "running",
        "version": "2.0.0",
        "capabilities": [
            "Route Planning & Optimization",
            "Delivery Manifests",
            "Real-time Route Updates",
            "Driver Assignment",
            "Efficient Delivery Sequencing"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint with manifest counts"""
    manifest_service = ManifestService()
    
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "2.0.0",
        "manifest_count": len(manifest_service.storage.get_all())
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host=settings.host, port=settings.port, reload=settings.debug
    )
