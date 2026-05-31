from typing import Dict, Any, List
from bfv.models.specs import ProjectSpecification
from bfv.ledger.escrow import ProjectEscrowLedger
from bfv.ledger.repository import CentralRepository
from bfv.ledger.backstop import InsuranceBackstop

class RegistryCoordinator:
    """
    The master interface for the Use Case 2 (Registry) persona.
    Orchestrates specs, math models, and the 3-layered solvency stacks seamlessly.
    """
    def __init__(self, registry_name: str, bfv_engine):
        self.registry_name = registry_name
        self.engine = bfv_engine
        
        # Initialize Layer 2 and Layer 3 institutional anchors
        self.central_repository = CentralRepository(repository_id=f"{registry_name}-L2-REPO")
        self.insurance_backstop = InsuranceBackstop(backstop_id=f"{registry_name}-L3-BACKSTOP")
        
        # Track all active Layer 1 ledgers
        self.project_ledgers: Dict[str, ProjectEscrowLedger] = {}

    def register_new_asset(self, spec: ProjectSpecification) -> Dict[str, Any]:
        """Runs the complete initial issuance pipeline across the entire solvency stack."""
        if spec.project_id in self.project_ledgers:
            raise ValueError(f"Project '{spec.project_id}' is already registered.")
            
        # 1. Compute initial BFV ratings profile
        math_results = self.engine.calculate_fair_value(**spec.to_engine_inputs())
        
        # 2. Instatiate Layer 1 Escrow account ledger
        ledger = ProjectEscrowLedger(project_id=spec.project_id, nominal_units=spec.nominal_units)
        ledger.initialize_allocation(math_results)
        
        # 3. Connect to the Layer 2 network umbrella
        self.project_ledgers[spec.project_id] = ledger
        self.central_repository.register_project_ledger(ledger)
        
        return ledger.get_summary()

    def process_monitoring_update(self, spec: ProjectSpecification, audit_event_name: str) -> Dict[str, Any]:
        """Processes an MRV performance update, trigger updates down the stack."""
        if spec.project_id not in self.project_ledgers:
            raise KeyError(f"Project '{spec.project_id}' is not registered under this registry.")
            
        # 1. Recalculate current math configurations
        updated_math = self.engine.calculate_fair_value(**spec.to_engine_inputs())
        
        # 2. Fire the state machine reconciliation check on Layer 1
        ledger = self.project_ledgers[spec.project_id]
        ledger.reconcile_state(updated_math, event_name=audit_event_name)
        
        return ledger.get_summary()

    def deploy_emergency_reinsurance(self, target_project_id: str, short_fall_units: float) -> dict:
        """
        Orchestrates an emergency rescue protocol by drawing capital out of 
        Layer 3 and injecting it into a depleted project via the Layer 2 pool.
        """
        # 1. Clear funds out of the L3 backstop
        emergency_funds = self.insurance_backstop.draw_down_backstop(short_fall_units)
        
        # 2. Inject funds directly into Layer 2 central buffer pool
        self.central_repository.central_buffer_pool += emergency_funds
        
        # 3. Issue emergency Layer 2 stabilizing bridge loan to target project
        loan_id = self.central_repository.issue_bridge_loan(target_project_id, emergency_funds)
        
        return {
            "emergency_funds_drawn_l3": emergency_funds,
            "bridge_loan_id_l2": loan_id,
            "ecosystem_status": self.get_registry_solvency_report()
        }

    def get_registry_solvency_report(self) -> Dict[str, Any]:
        """Compiles a master structural reporting sheet of the registry ecosystem."""
        total_nominal = sum(l.nominal_units for l in self.project_ledgers.values())
        total_circulating = sum(l.circulating_balance for l in self.project_ledgers.values())
        total_escrow = sum(l.escrow_balance for l in self.project_ledgers.values())
        
        return {
            "registry_name": self.registry_name,
            "total_registered_projects": len(self.project_ledgers),
            "total_portfolio_nominal_capacity": round(total_nominal, 2),
            "aggregate_circulating_supply": round(total_circulating, 2),
            "aggregate_escrow_reserve_pool": round(total_escrow, 2),
            "layer_2_central_buffer": round(self.central_repository.central_buffer_pool, 2),
            "layer_3_insurance_capital": round(self.insurance_backstop.available_capital, 2)
        }
