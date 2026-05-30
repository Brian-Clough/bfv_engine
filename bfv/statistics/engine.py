from typing import List, Dict, Any
class BFVEngine:
    def __init__(self, execution_model, permanence_model):
        self.execution_model = execution_model
        self.permanence_model = permanence_model
    def calculate_fair_value(self, milestones: List[int], p_science: float, historical_reversal_rate_100yr: float, k_shape: float, co_benefit_scalar: float, nominal_units: float = 1.0) -> Dict[str, Any]:
        p_execution = self.execution_model.evaluate_posterior_mean(milestones)
        p_permanence = self.permanence_model.calculate_survival_probability(historical_reversal_rate_100yr, k_shape)
        expected_delivery = float(p_execution * p_science * p_permanence)
        bfv_unit = float(expected_delivery + co_benefit_scalar)
        integrity_gap = max(0.0, 1.0 - bfv_unit)
        return {
            "p_execution": p_execution, "p_science": p_science, "p_permanence": p_permanence,
            "expected_delivery_coefficient": expected_delivery, "bfv_unit_value": bfv_unit,
            "integrity_gap": integrity_gap, "issuable_bfv_units": nominal_units * bfv_unit,
            "escrow_retained_units": nominal_units * integrity_gap
        }
