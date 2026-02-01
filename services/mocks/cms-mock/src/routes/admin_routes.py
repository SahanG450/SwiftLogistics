from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from ..models.schemas import Admin, AdminCreate, AdminUpdate, AdminRole, ErrorResponse
from ..services.admin_service import AdminService

router = APIRouter(prefix="/admins", tags=["admins"])
admin_service = AdminService()


@router.get("/", response_model=List[Admin])
async def get_all_admins(
    role: Optional[AdminRole] = Query(None, description="Filter admins by role")
):
    """Get all admins, optionally filtered by role"""
    if role:
        return admin_service.get_admins_by_role(role)
    return admin_service.get_all_admins()


@router.get("/{admin_id}", response_model=Admin, responses={404: {"model": ErrorResponse}})
async def get_admin(admin_id: str):
    """Get a specific admin by ID"""
    admin = admin_service.get_admin_by_id(admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    return admin


@router.post("/", response_model=Admin, status_code=status.HTTP_201_CREATED)
async def create_admin(admin: AdminCreate):
    """Create a new admin"""
    return admin_service.create_admin(admin)


@router.put("/{admin_id}", response_model=Admin, responses={404: {"model": ErrorResponse}})
async def update_admin(admin_id: str, admin: AdminUpdate):
    """Update an admin"""
    updated_admin = admin_service.update_admin(admin_id, admin)
    if not updated_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    return updated_admin


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(admin_id: str):
    """Delete an admin"""
    deleted = admin_service.delete_admin(admin_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    return None
