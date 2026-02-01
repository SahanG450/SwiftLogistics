from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.schemas import Customer, CustomerCreate, CustomerUpdate, ErrorResponse
from ..services.cms_service import cms_service

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("/", response_model=List[Customer])
async def get_all_customers():
    """Get all customers"""
    return cms_service.get_all_customers()


@router.get(
    "/{customer_id}", response_model=Customer, responses={404: {"model": ErrorResponse}}
)
async def get_customer(customer_id: str):
    """Get customer by ID"""
    customer = cms_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )
    return customer


@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate):
    """Create new customer"""
    return cms_service.create_customer(customer)


@router.put(
    "/{customer_id}", response_model=Customer, responses={404: {"model": ErrorResponse}}
)
async def update_customer(customer_id: str, customer: CustomerUpdate):
    """Update existing customer"""
    updated_customer = cms_service.update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )
    return updated_customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: str):
    """Delete customer"""
    success = cms_service.delete_customer(customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )
    return None


@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CMS Mock Service",
        "total_customers": len(cms_service.customers),
    }
