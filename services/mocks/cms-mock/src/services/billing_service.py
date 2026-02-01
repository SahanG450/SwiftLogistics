from typing import List, Optional
from datetime import datetime
import uuid

from ..utils.file_storage import FileStorage
from ..models.schemas import BillingInvoice, BillingCreate, BillingUpdate


class BillingService:
    def __init__(self):
        self.storage = FileStorage(data_dir="data", filename="billing")
        self._init_mock_data()
        self.invoice_counter = self._get_next_invoice_number()

    def _get_next_invoice_number(self) -> int:
        """Get the next invoice number"""
        invoices = self.storage.get_all()
        if not invoices:
            return 10001

        max_num = 10001
        for invoice in invoices.values():
            try:
                parts = invoice.get("invoice_number", "").split("-")
                if len(parts) == 3:
                    num = int(parts[2])
                    max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
        return max_num + 1

    def _generate_invoice_number(self) -> str:
        """Generate invoice number: INV-YYYY-NNNNN"""
        year = datetime.now().year
        invoice_num = f"INV-{year}-{self.invoice_counter:05d}"
        self.invoice_counter += 1
        return invoice_num

    def _calculate_billing_amount(
        self, base_rate: float, total_deliveries: int, volume_discount: float = 0.0
    ) -> float:
        """Calculate total billing amount"""
        subtotal = base_rate * total_deliveries
        discount_amount = subtotal * (volume_discount / 100)
        return subtotal - discount_amount

    def _init_mock_data(self):
        """Initialize with sample billing records"""
        if not self.storage.get_all():
            # Invoice for Daraz - January 2026
            invoice1_id = str(uuid.uuid4())
            invoice1 = {
                "id": invoice1_id,
                "invoice_number": "INV-2026-10001",
                "client_id": "client-001",
                "client_name": "Daraz Lanka",
                "contract_id": "CON-5001",
                "billing_period_start": "2026-01-01",
                "billing_period_end": "2026-01-31",
                "total_deliveries": 1450,
                "successful_deliveries": 1398,
                "failed_deliveries": 52,
                "total_amount": 308625.0,  # 1450 * 250 with 15% discount
                "paid_amount": 308625.0,
                "payment_status": "paid",
                "payment_date": "2026-02-15",
                "notes": "January billing - High volume promotional event",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            # Invoice for Kapruka - pending
            invoice2_id = str(uuid.uuid4())
            invoice2 = {
                "id": invoice2_id,
                "invoice_number": "INV-2026-10002",
                "client_id": "client-002",
                "client_name": "Kapruka.com",
                "contract_id": "CON-5002",
                "billing_period_start": "2026-01-01",
                "billing_period_end": "2026-01-31",
                "total_deliveries": 856,
                "successful_deliveries": 834,
                "failed_deliveries": 22,
                "total_amount": 205440.0,  # 856 * 300 with 20% discount
                "paid_amount": 0.0,
                "payment_status": "pending",
                "payment_date": None,
                "notes": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            self.storage.create(invoice1_id, invoice1)
            self.storage.create(invoice2_id, invoice2)

    def create_invoice(
        self,
        billing_data: BillingCreate,
        base_rate: float = 250.0,
        volume_discount: float = 0.0,
    ) -> BillingInvoice:
        """Create a new billing invoice"""
        invoice_id = str(uuid.uuid4())
        invoice_number = self._generate_invoice_number()

        total_amount = self._calculate_billing_amount(
            base_rate, billing_data.total_deliveries, volume_discount
        )

        now = datetime.now().isoformat()
        invoice_dict = {
            "id": invoice_id,
            "invoice_number": invoice_number,
            **billing_data.model_dump(),
            "total_amount": total_amount,
            "paid_amount": 0.0,
            "payment_status": "pending",
            "payment_date": None,
            "notes": None,
            "created_at": now,
            "updated_at": now,
        }

        self.storage.create(invoice_id, invoice_dict)
        return BillingInvoice(**invoice_dict)

    def get_invoice(self, invoice_id: str) -> Optional[BillingInvoice]:
        """Get a specific invoice by ID"""
        invoice_data = self.storage.get(invoice_id)
        if invoice_data:
            return BillingInvoice(**invoice_data)
        return None

    def get_all_invoices(
        self,
        client_id: Optional[str] = None,
        payment_status: Optional[str] = None,
    ) -> List[BillingInvoice]:
        """Get all invoices with optional filtering"""
        invoices = self.storage.get_all()
        invoice_list = [BillingInvoice(**invoice) for invoice in invoices.values()]

        if client_id:
            invoice_list = [i for i in invoice_list if i.client_id == client_id]
        if payment_status:
            invoice_list = [
                i for i in invoice_list if i.payment_status == payment_status
            ]

        return invoice_list

    def update_invoice(
        self, invoice_id: str, billing_update: BillingUpdate
    ) -> Optional[BillingInvoice]:
        """Update an existing invoice"""
        existing_invoice = self.storage.get(invoice_id)
        if not existing_invoice:
            return None

        update_data = billing_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()

        updated_invoice = {**existing_invoice, **update_data}
        self.storage.update(invoice_id, updated_invoice)

        return BillingInvoice(**updated_invoice)

    def delete_invoice(self, invoice_id: str) -> bool:
        """Delete an invoice"""
        return self.storage.delete(invoice_id)

    def record_payment(
        self, invoice_id: str, payment_amount: float, payment_date: Optional[str] = None
    ) -> Optional[BillingInvoice]:
        """Record a payment for an invoice"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return None

        new_paid_amount = invoice.paid_amount + payment_amount

        # Determine payment status
        if new_paid_amount >= invoice.total_amount:
            payment_status = "paid"
        elif new_paid_amount > 0:
            payment_status = "partial"
        else:
            payment_status = "pending"

        update = BillingUpdate(
            paid_amount=new_paid_amount,
            payment_status=payment_status,
            payment_date=payment_date or datetime.now().isoformat(),
        )

        return self.update_invoice(invoice_id, update)
