from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.settings import settings
from src.routes.cms_routes import router as cms_router
from src.routes.driver_routes import router as driver_router
from src.routes.client_routes import router as client_router
from src.routes.admin_routes import router as admin_router
from src.routes.order_routes import router as order_router
from src.routes.contract_routes import router as contract_router
from src.routes.billing_routes import router as billing_router
from src.services.cms_service import CMSService
from src.services.driver_service import DriverService
from src.services.client_service import ClientService
from src.services.admin_service import AdminService
from src.services.order_service import OrderService
from src.services.contract_service import ContractService
from src.services.billing_service import BillingService

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Client Management System Mock Service for Swift Logistics - Legacy SOAP-based system (REST simulation)",
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
app.include_router(cms_router)
app.include_router(driver_router)
app.include_router(client_router)
app.include_router(admin_router)
app.include_router(order_router)
app.include_router(contract_router)
app.include_router(billing_router)


@app.get("/")
async def root():
    """Root endpoint - CMS Service Information"""
    return {
        "service": settings.app_name,
        "description": "Client Management System (Legacy SOAP-based - REST simulation)",
        "status": "running",
        "version": "2.0.0",
        "capabilities": [
            "Order Intake & Management",
            "Client Contracts",
            "Billing & Invoicing",
            "Customer Management",
            "Driver Management"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint with entity counts"""
    customer_service = CMSService()
    driver_service = DriverService()
    client_service = ClientService()
    admin_service = AdminService()
    order_service = OrderService()
    contract_service = ContractService()
    billing_service = BillingService()

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "2.0.0",
        "entity_counts": {
            "customers": len(customer_service.storage.get_all()),
            "drivers": len(driver_service.storage.get_all()),
            "clients": len(client_service.storage.get_all()),
            "admins": len(admin_service.storage.get_all()),
            "orders": len(order_service.storage.get_all()),
            "contracts": len(contract_service.storage.get_all()),
            "invoices": len(billing_service.storage.get_all()),
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host=settings.host, port=settings.port, reload=settings.debug
    )
