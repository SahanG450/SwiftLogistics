from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..models.schemas import (
    DeliveryManifest,
    ManifestCreate,
    ManifestUpdate,
    ManifestStatus,
    DeliveryStatus,
)
from ..services.manifest_service import ManifestService

router = APIRouter(prefix="/api/manifests", tags=["Delivery Manifests"])
manifest_service = ManifestService()


@router.get("/", response_model=List[DeliveryManifest])
async def get_all_manifests(
    driver_id: Optional[str] = Query(None, description="Filter by driver ID"),
    status: Optional[ManifestStatus] = Query(None, description="Filter by manifest status"),
    delivery_date: Optional[str] = Query(None, description="Filter by delivery date (YYYY-MM-DD)"),
):
    """Get all delivery manifests with optional filtering"""
    return manifest_service.get_all_manifests(
        driver_id=driver_id, status=status, delivery_date=delivery_date
    )


@router.get("/{manifest_id}", response_model=DeliveryManifest)
async def get_manifest(manifest_id: str):
    """Get a specific delivery manifest by ID"""
    manifest = manifest_service.get_manifest(manifest_id)
    if not manifest:
        raise HTTPException(
            status_code=404, detail=f"Manifest with ID {manifest_id} not found"
        )
    return manifest


@router.post("/", response_model=DeliveryManifest, status_code=201)
async def create_manifest(manifest: ManifestCreate):
    """Create a new delivery manifest"""
    return manifest_service.create_manifest(manifest)


@router.put("/{manifest_id}", response_model=DeliveryManifest)
async def update_manifest(manifest_id: str, manifest: ManifestUpdate):
    """Update an existing manifest"""
    updated_manifest = manifest_service.update_manifest(manifest_id, manifest)
    if not updated_manifest:
        raise HTTPException(
            status_code=404, detail=f"Manifest with ID {manifest_id} not found"
        )
    return updated_manifest


@router.delete("/{manifest_id}", status_code=204)
async def delete_manifest(manifest_id: str):
    """Delete a manifest"""
    if not manifest_service.delete_manifest(manifest_id):
        raise HTTPException(
            status_code=404, detail=f"Manifest with ID {manifest_id} not found"
        )


@router.post("/{manifest_id}/assign", response_model=DeliveryManifest)
async def assign_manifest(manifest_id: str):
    """Assign manifest to driver (move from draft to assigned)"""
    manifest = manifest_service.assign_manifest(manifest_id)
    if not manifest:
        raise HTTPException(
            status_code=404, detail=f"Manifest with ID {manifest_id} not found"
        )
    return manifest


@router.post("/{manifest_id}/start", response_model=DeliveryManifest)
async def start_manifest(manifest_id: str):
    """Start manifest delivery (driver begins route)"""
    manifest = manifest_service.start_manifest(manifest_id)
    if not manifest:
        raise HTTPException(
            status_code=404, detail=f"Manifest with ID {manifest_id} not found"
        )
    return manifest


@router.post("/{manifest_id}/complete", response_model=DeliveryManifest)
async def complete_manifest(manifest_id: str):
    """Mark manifest as completed"""
    manifest = manifest_service.complete_manifest(manifest_id)
    if not manifest:
        raise HTTPException(
            status_code=404, detail=f"Manifest with ID {manifest_id} not found"
        )
    return manifest


@router.put("/{manifest_id}/deliveries/{order_id}", response_model=DeliveryManifest)
async def update_delivery_status(
    manifest_id: str,
    order_id: str,
    status: DeliveryStatus = Query(..., description="New delivery status"),
):
    """Update the status of a specific delivery in the manifest"""
    manifest = manifest_service.update_delivery_status(manifest_id, order_id, status)
    if not manifest:
        raise HTTPException(
            status_code=404,
            detail=f"Manifest with ID {manifest_id} or order {order_id} not found",
        )
    return manifest
