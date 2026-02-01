from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.settings import settings
from src.routes.ros_routes import router as ros_router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Route Optimization System Mock Service for Swift Logistics",
    version="1.0.0",
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


@app.get("/")
async def root():
    """Root endpoint"""
    return {"service": settings.app_name, "status": "running", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.app_name}


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host=settings.host, port=settings.port, reload=settings.debug
    )
