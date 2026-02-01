from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from ..models.schemas import Client, ClientCreate, ClientUpdate, MembershipLevel, ErrorResponse
from ..services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])
client_service = ClientService()


@router.get("/", response_model=List[Client])
async def get_all_clients(
    membership_level: Optional[MembershipLevel] = Query(None, description="Filter clients by membership level")
):
    """Get all clients, optionally filtered by membership level"""
    if membership_level:
        return client_service.get_clients_by_membership(membership_level)
    return client_service.get_all_clients()


@router.get("/{client_id}", response_model=Client, responses={404: {"model": ErrorResponse}})
async def get_client(client_id: str):
    """Get a specific client by ID"""
    client = client_service.get_client_by_id(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id {client_id} not found"
        )
    return client


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate):
    """Create a new client"""
    return client_service.create_client(client)


@router.put("/{client_id}", response_model=Client, responses={404: {"model": ErrorResponse}})
async def update_client(client_id: str, client: ClientUpdate):
    """Update a client"""
    updated_client = client_service.update_client(client_id, client)
    if not updated_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id {client_id} not found"
        )
    return updated_client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: str):
    """Delete a client"""
    deleted = client_service.delete_client(client_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id {client_id} not found"
        )
    return None
