from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..models.schemas import Contract, ContractCreate, ContractUpdate, ContractStatus
from ..services.contract_service import ContractService

router = APIRouter(prefix="/api/contracts", tags=["Contracts"])
contract_service = ContractService()


@router.get("/", response_model=List[Contract])
async def get_all_contracts(
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    status: Optional[ContractStatus] = Query(None, description="Filter by contract status"),
):
    """Get all contracts with optional filtering"""
    return contract_service.get_all_contracts(client_id=client_id, status=status)


@router.get("/{contract_id}", response_model=Contract)
async def get_contract(contract_id: str):
    """Get a specific contract by ID"""
    contract = contract_service.get_contract(contract_id)
    if not contract:
        raise HTTPException(
            status_code=404, detail=f"Contract with ID {contract_id} not found"
        )
    return contract


@router.post("/", response_model=Contract, status_code=201)
async def create_contract(contract: ContractCreate):
    """Create a new contract"""
    return contract_service.create_contract(contract)


@router.put("/{contract_id}", response_model=Contract)
async def update_contract(contract_id: str, contract: ContractUpdate):
    """Update an existing contract"""
    updated_contract = contract_service.update_contract(contract_id, contract)
    if not updated_contract:
        raise HTTPException(
            status_code=404, detail=f"Contract with ID {contract_id} not found"
        )
    return updated_contract


@router.delete("/{contract_id}", status_code=204)
async def delete_contract(contract_id: str):
    """Delete a contract"""
    if not contract_service.delete_contract(contract_id):
        raise HTTPException(
            status_code=404, detail=f"Contract with ID {contract_id} not found"
        )


@router.post("/{contract_id}/activate", response_model=Contract)
async def activate_contract(contract_id: str):
    """Activate a contract"""
    contract = contract_service.activate_contract(contract_id)
    if not contract:
        raise HTTPException(
            status_code=404, detail=f"Contract with ID {contract_id} not found"
        )
    return contract


@router.post("/{contract_id}/suspend", response_model=Contract)
async def suspend_contract(contract_id: str):
    """Suspend a contract"""
    contract = contract_service.suspend_contract(contract_id)
    if not contract:
        raise HTTPException(
            status_code=404, detail=f"Contract with ID {contract_id} not found"
        )
    return contract


@router.post("/{contract_id}/terminate", response_model=Contract)
async def terminate_contract(contract_id: str):
    """Terminate a contract"""
    contract = contract_service.terminate_contract(contract_id)
    if not contract:
        raise HTTPException(
            status_code=404, detail=f"Contract with ID {contract_id} not found"
        )
    return contract
