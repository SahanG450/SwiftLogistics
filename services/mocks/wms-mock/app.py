from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.settings import settings
from src.routes.wms_routes import router as wms_router
from src.routes.package_routes import router as package_router
from src.services.package_service import PackageService

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Warehouse Management System Mock Service for Swift Logistics - Package tracking from receipt to loading",
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
app.include_router(wms_router)
app.include_router(package_router)


@app.get("/")
async def root():
    """Root endpoint - WMS Service Information"""
    return {
        "service": settings.app_name,
        "description": "Warehouse Management System - Package tracking from receipt to loading",
        "status": "running",
        "version": "2.0.0",
        "capabilities": [
            "Package Receiving",
            "Quality Inspection",
            "Warehouse Storage",
            "Package Tracking",
            "Vehicle Loading"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint with package counts"""
    package_service = PackageService()
    
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "2.0.0",
        "package_count": len(package_service.storage.get_all())
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host=settings.host, port=settings.port, reload=settings.debug
    )
