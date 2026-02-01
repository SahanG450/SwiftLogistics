from typing import List, Optional
from datetime import datetime
import uuid

from ..utils.file_storage import FileStorage
from ..models.schemas import Contract, ContractCreate, ContractUpdate, ContractStatus


class ContractService:
    def __init__(self):
        self.storage = FileStorage(data_dir="data", filename="contracts")
        self._init_mock_data()
        self.contract_counter = self._get_next_contract_number()

    def _get_next_contract_number(self) -> int:
        """Get the next contract number"""
        contracts = self.storage.get_all()
        if not contracts:
            return 5001

        max_num = 5001
        for contract in contracts.values():
            try:
                parts = contract.get("contract_number", "").split("-")
                if len(parts) == 2:
                    num = int(parts[1])
                    max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
        return max_num + 1

    def _generate_contract_number(self) -> str:
        """Generate contract number: CON-NNNN"""
        contract_num = f"CON-{self.contract_counter:04d}"
        self.contract_counter += 1
        return contract_num

    def _init_mock_data(self):
        """Initialize with sample contracts"""
        if not self.storage.get_all():
            # Contract for Daraz
            contract1_id = str(uuid.uuid4())
            contract1 = {
                "id": contract1_id,
                "contract_number": "CON-5001",
                "client_id": "client-001",
                "client_name": "Daraz Lanka",
                "contract_type": "monthly",
                "status": "active",
                "start_date": "2026-01-01",
                "end_date": "2026-12-31",
                "base_rate": 250.0,  # LKR per delivery
                "volume_discount": 15.0,  # 15% discount for >1000 deliveries/month
                "payment_terms": "NET-30",
                "special_terms": "Priority support during promotional events",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            # Contract for Kapruka
            contract2_id = str(uuid.uuid4())
            contract2 = {
                "id": contract2_id,
                "contract_number": "CON-5002",
                "client_id": "client-002",
                "client_name": "Kapruka.com",
                "contract_type": "tiered",
                "status": "active",
                "start_date": "2025-06-01",
                "end_date": "2027-05-31",
                "base_rate": 300.0,
                "volume_discount": 20.0,
                "payment_terms": "NET-15",
                "special_terms": "Same-day delivery option available",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

            self.storage.create(contract1_id, contract1)
            self.storage.create(contract2_id, contract2)

    def create_contract(self, contract_data: ContractCreate) -> Contract:
        """Create a new contract"""
        contract_id = str(uuid.uuid4())
        contract_number = self._generate_contract_number()

        now = datetime.now().isoformat()
        contract_dict = {
            "id": contract_id,
            "contract_number": contract_number,
            **contract_data.model_dump(),
            "status": ContractStatus.DRAFT,
            "created_at": now,
            "updated_at": now,
        }

        self.storage.create(contract_id, contract_dict)
        return Contract(**contract_dict)

    def get_contract(self, contract_id: str) -> Optional[Contract]:
        """Get a specific contract by ID"""
        contract_data = self.storage.get(contract_id)
        if contract_data:
            return Contract(**contract_data)
        return None

    def get_all_contracts(
        self,
        client_id: Optional[str] = None,
        status: Optional[ContractStatus] = None,
    ) -> List[Contract]:
        """Get all contracts with optional filtering"""
        contracts = self.storage.get_all()
        contract_list = [Contract(**contract) for contract in contracts.values()]

        if client_id:
            contract_list = [c for c in contract_list if c.client_id == client_id]
        if status:
            contract_list = [c for c in contract_list if c.status == status]

        return contract_list

    def update_contract(
        self, contract_id: str, contract_update: ContractUpdate
    ) -> Optional[Contract]:
        """Update an existing contract"""
        existing_contract = self.storage.get(contract_id)
        if not existing_contract:
            return None

        update_data = contract_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()

        updated_contract = {**existing_contract, **update_data}
        self.storage.update(contract_id, updated_contract)

        return Contract(**updated_contract)

    def delete_contract(self, contract_id: str) -> bool:
        """Delete a contract"""
        return self.storage.delete(contract_id)

    def activate_contract(self, contract_id: str) -> Optional[Contract]:
        """Activate a contract"""
        update = ContractUpdate(status=ContractStatus.ACTIVE)
        return self.update_contract(contract_id, update)

    def suspend_contract(self, contract_id: str) -> Optional[Contract]:
        """Suspend a contract"""
        update = ContractUpdate(status=ContractStatus.SUSPENDED)
        return self.update_contract(contract_id, update)

    def terminate_contract(self, contract_id: str) -> Optional[Contract]:
        """Terminate a contract"""
        update = ContractUpdate(status=ContractStatus.TERMINATED)
        return self.update_contract(contract_id, update)
