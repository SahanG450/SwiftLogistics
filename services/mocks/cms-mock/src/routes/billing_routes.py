from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..models.schemas import BillingInvoice, BillingCreate, BillingUpdate
from ..services.billing_service import BillingService

router = APIRouter(prefix="/api/billing", tags=["Billing"])
billing_service = BillingService()


@router.get("/", response_model=List[BillingInvoice])
async def get_all_invoices(
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    payment_status: Optional[str] = Query(None, description="Filter by payment status"),
):
    """Get all billing invoices with optional filtering"""
    return billing_service.get_all_invoices(client_id=client_id, payment_status=payment_status)


@router.get("/{invoice_id}", response_model=BillingInvoice)
async def get_invoice(invoice_id: str):
    """Get a specific invoice by ID"""
    invoice = billing_service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=404, detail=f"Invoice with ID {invoice_id} not found"
        )
    return invoice


@router.post("/", response_model=BillingInvoice, status_code=201)
async def create_invoice(
    billing: BillingCreate,
    base_rate: float = Query(250.0, description="Base rate per delivery in LKR"),
    volume_discount: float = Query(0.0, description="Volume discount percentage"),
):
    """Create a new billing invoice"""
    return billing_service.create_invoice(billing, base_rate, volume_discount)


@router.put("/{invoice_id}", response_model=BillingInvoice)
async def update_invoice(invoice_id: str, billing: BillingUpdate):
    """Update an existing invoice"""
    updated_invoice = billing_service.update_invoice(invoice_id, billing)
    if not updated_invoice:
        raise HTTPException(
            status_code=404, detail=f"Invoice with ID {invoice_id} not found"
        )
    return updated_invoice


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(invoice_id: str):
    """Delete an invoice"""
    if not billing_service.delete_invoice(invoice_id):
        raise HTTPException(
            status_code=404, detail=f"Invoice with ID {invoice_id} not found"
        )


@router.post("/{invoice_id}/record-payment", response_model=BillingInvoice)
async def record_payment(
    invoice_id: str,
    payment_amount: float = Query(..., description="Payment amount in LKR"),
    payment_date: Optional[str] = Query(None, description="Payment date (ISO format)"),
):
    """Record a payment for an invoice"""
    invoice = billing_service.record_payment(invoice_id, payment_amount, payment_date)
    if not invoice:
        raise HTTPException(
            status_code=404, detail=f"Invoice with ID {invoice_id} not found"
        )
    return invoice
