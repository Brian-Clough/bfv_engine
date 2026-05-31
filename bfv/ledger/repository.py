from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Any
from bfv.ledger.escrow import ProjectEscrowLedger

@dataclass
class BridgeLoanRecord:
    """Tracks a Layer 2 credit insurance injection extended to an underperforming asset."""
    loan_id: str
    project_id: str
    principal_units: float
    outstanding_balance: float
    issued_timestamp: str
    status: str  # 'ACTIVE', 'REPAID', 'DEFAULTED'

class CentralRepository:
    """
    Implements Layer 2 Central Repository mechanics. Operates a mutualized credit
    insurance bridge across separate project escrows to absorb localized shocks.
    """
    def __init__(self, repository_id: str):
        self.repository_id = repository_id
        self.project_ledgers: Dict[str, ProjectEscrowLedger] = {}
        
        # Central Pool state tracking
        self.central_buffer_pool = 0.0
        self.active_loans: Dict[str, BridgeLoanRecord] = {}
        self.loan_counter = 0

    def register_project_ledger(self, ledger: ProjectEscrowLedger):
        """Links a Layer 1 ledger into the Layer 2 repository umbrella."""
        self.project_ledgers[ledger.project_id] = ledger

    def contribute_to_buffer(self, project_id: str, units: float) -> float:
        """
        Tax or deduction allocation that shifts units from a specific Layer 1 escrow 
        into the shared Layer 2 insurance pool.
        """
        if project_id not in self.project_ledgers:
            raise ValueError(f"Project '{project_id}' is not registered under this repository.")
            
        ledger = self.project_ledgers[project_id]
        if ledger.escrow_balance < units:
            raise ValueError(f"Insufficient escrow balance in project {project_id} to complete contribution.")
            
        # Adjust cross-layer credit ledger positions
        ledger.escrow_balance -= units
        self.central_buffer_pool += units
        
        # Log the debit event on Layer 1
        ledger._add_log(
            event_type="L2_BUFFER_CONTRIBUTION",
            circ_delta=0.0,
            esc_delta=-units,
            bfv=ledger.circulating_balance / ledger.nominal_units if ledger.nominal_units > 0 else 0.0,
            description=f"Transferred {units:.2f} reserve credits to Central Repository Layer 2 pool."
        )
        return self.central_buffer_pool

    def issue_bridge_loan(self, project_id: str, units: float) -> str:
        """
        Extends a liquidity credit bridge loan to a project suffering a localized
        deficit, injecting credits directly into its circulating market balance.
        """
        if self.central_buffer_pool < units:
            raise ValueError(f"Insufficient funds in Central Repository buffer pool ({self.central_buffer_pool:.2f}).")
            
        if project_id not in self.project_ledgers:
            raise ValueError(f"Project '{project_id}' is not registered under this repository.")
            
        # Deduct from central pool and credit Layer 1 circulating balance
        self.central_buffer_pool -= units
        ledger = self.project_ledgers[project_id]
        ledger.circulating_balance += units
        
        # Generate tracking record
        self.loan_counter += 1
        loan_id = f"LN-{self.loan_counter:04d}"
        
        self.active_loans[loan_id] = BridgeLoanRecord(
            loan_id=loan_id,
            project_id=project_id,
            principal_units=units,
            outstanding_balance=units,
            issued_timestamp=datetime.now(timezone.utc).isoformat(),
            status="ACTIVE"
        )
        
        # Log the credit event on the recipient Layer 1 ledger
        ledger._add_log(
            event_type="L2_BRIDGE_LOAN_INJECTION",
            circ_delta=units,
            esc_delta=0.0,
            bfv=ledger.circulating_balance / ledger.nominal_units,
            description=f"Received {units:.2f} units bridge loan from Layer 2 Central Pool (Loan ID: {loan_id})."
        )
        return loan_id

    def process_loan_repayment(self, loan_id: str, units: float) -> float:
        """
        Claws back units from an asset's circulating balance to pay down its
        outstanding Layer 2 insurance deficit as performance risks clear up.
        """
        if loan_id not in self.active_loans:
            raise KeyError(f"Loan ID '{loan_id}' not found.")
            
        loan = self.active_loans[loan_id]
        if loan.status != "ACTIVE":
            raise ValueError(f"Loan '{loan_id}' is already closed ({loan.status}).")
            
        ledger = self.project_ledgers[loan.project_id]
        repayment_amount = min(units, loan.outstanding_balance, ledger.circulating_balance)
        
        # Shift balances back to central repository pool
        ledger.circulating_balance -= repayment_amount
        loan.outstanding_balance -= repayment_amount
        self.central_buffer_pool += repayment_amount
        
        if loan.outstanding_balance <= 1e-6:
            loan.status = "REPAID"
            
        ledger._add_log(
            event_type="L2_BRIDGE_LOAN_REPAYMENT",
            circ_delta=-repayment_amount,
            esc_delta=0.0,
            bfv=ledger.circulating_balance / ledger.nominal_units,
            description=f"Repaid {repayment_amount:.2f} units toward Layer 2 bridge loan {loan_id}. Outstanding: {loan.outstanding_balance:.2f}."
        )
        return loan.outstanding_balance

    def get_repository_status(self) -> Dict[str, Any]:
        """Compiles a status map of the cross-project insurance ecosystem."""
        return {
            "repository_id": self.repository_id,
            "central_buffer_pool_balance": round(self.central_buffer_pool, 2),
            "total_registered_projects": len(self.project_ledgers),
            "active_loans_count": sum(1 for l in self.active_loans.values() if l.status == "ACTIVE"),
            "closed_loans_count": sum(1 for l in self.active_loans.values() if l.status == "REPAID")
        }
