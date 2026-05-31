from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any

@dataclass
class LedgerTransaction:
    """Records an immutable ledger entry event for auditing project adjustments."""
    timestamp: str
    event_type: str            # e.g., 'INITIAL_ALLOCATION', 'VALUE_RELEASE', 'RISK_ADJUSTMENT'
    circulating_change: float
    escrow_change: float
    calculated_bfv: float
    description: str

class ProjectEscrowLedger:
    """
    Implements Layer 1 Project Escrow ledger mechanics. Tracks circulating 
    vs reserved balances and provides transactional adjustment interfaces.
    """
    def __init__(self, project_id: str, nominal_units: float):
        self.project_id = project_id
        self.nominal_units = nominal_units
        
        # State Balances
        self.circulating_balance = 0.0
        self.escrow_balance = 0.0
        
        # Audit Trail Log
        self.history: List[LedgerTransaction] = []

    def _add_log(self, event_type: str, circ_delta: float, esc_delta: float, bfv: float, description: str):
        """Helper to append an immutable transaction log entry."""
        self.history.append(LedgerTransaction(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            circulating_change=round(circ_delta, 4),
            escrow_change=round(esc_delta, 4),
            calculated_bfv=round(bfv, 4),
            description=description
        ))

    def initialize_allocation(self, engine_results: Dict[str, Any]):
        """Establishes the base token parameters derived from the core math engine."""
        bfv = engine_results["bfv_unit_value"]
        
        self.circulating_balance = engine_results["issuable_bfv_units"]
        self.escrow_balance = engine_results["escrow_retained_units"]
        
        self._add_log(
            event_type="INITIAL_ALLOCATION",
            circ_delta=self.circulating_balance,
            esc_delta=self.escrow_balance,
            bfv=bfv,
            description=f"Initialized asset with BFV={bfv:.4f} and nominal allocation of {self.nominal_units} tons."
        )

    def reconcile_state(self, engine_results: Dict[str, Any], event_name: str = "SYSTEM_RECONCILIATION"):
        """
        Compares active ledger balances against updated math engine metrics,
        executing a value release or escrow absorption depending on risk trajectory.
        """
        bfv = engine_results["bfv_unit_value"]
        
        # Calculate where balances *should* be based on the new math
        target_circulating = engine_results["issuable_bfv_units"]
        target_escrow = engine_results["escrow_retained_units"]
        
        # Determine necessary variance adjustments
        circ_delta = target_circulating - self.circulating_balance
        esc_delta = target_escrow - self.escrow_balance
        
        # If variances are zero, skip writing noise to ledger history
        if abs(circ_delta) < 1e-6 and abs(esc_delta) < 1e-6:
            return False
            
        # Execute ledger update state transition
        self.circulating_balance = target_circulating
        self.escrow_balance = target_escrow
        
        # Classify the type of transaction adjustment taking place
        event_type = "VALUE_RELEASE" if circ_delta > 0 else "ESCROW_ABSORPTION"
        desc = (
            f"Reconciliation via '{event_name}'. "
            f"Circulating change: {circ_delta:+.2f}, Escrow change: {esc_delta:+.2f}."
        )
        
        self._add_log(event_type, circ_delta, esc_delta, bfv, desc)
        return True

    def get_summary(self) -> Dict[str, Any]:
        """Returns structural balances for reporting applications."""
        return {
            "project_id": self.project_id,
            "nominal_pool": self.nominal_units,
            "circulating_balance": round(self.circulating_balance, 2),
            "escrow_balance": round(self.escrow_balance, 2),
            "total_accounted": round(self.circulating_balance + self.escrow_balance, 2),
            "transaction_count": len(self.history)
        }
