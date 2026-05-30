import numpy as np
from typing import List, Dict, Any
from bfv.statistics.inputs import ProbabilisticInput

class BFVEngine:
    def __init__(self, execution_model, permanence_model):
        self.execution_model = execution_model
        self.permanence_model = permanence_model
        
    def calculate_fair_value(
        self, 
        milestones: List[int], 
        science_input: Any, 
        historical_reversal_rate_100yr: float,
        k_shape: float,
        co_benefit_input: Any,
        nominal_units: float = 1.0,
        num_simulation_samples: int = 5000
    ) -> Dict[str, Any]:
        """
        Calculates BFV utilizing full uncertainty accounting or point-estimates dynamically.
        """
        # 1. Parse custom Science and Co-Benefit entry shapes into standardized Monte Carlo vectors
        science_dist = ProbabilisticInput(science_input, num_samples=num_simulation_samples)
        cobenefit_dist = ProbabilisticInput(co_benefit_input, num_samples=num_simulation_samples)
        
        # 2. Extract standard cookie-cutter Bayesian updates
        p_execution_mean = self.execution_model.evaluate_posterior_mean(milestones)
        p_permanence_mean = self.permanence_model.calculate_survival_probability(
            historical_reversal_rate_100yr, k_shape
        )
        
        # Determine if we can execute straight fast-path point math or must run Monte Carlo chains
        if science_dist.is_point_estimate and cobenefit_dist.is_point_estimate:
            # --- FAST PATH: Point Estimate Execution ---
            expected_delivery = float(p_execution_mean * science_dist.evaluate_mean() * p_permanence_mean)
            bfv_unit = float(expected_delivery + cobenefit_dist.evaluate_mean())
            integrity_gap = max(0.0, 1.0 - bfv_unit)
            
            return {
                "p_execution_mean": p_execution_mean,
                "p_permanence_mean": p_permanence_mean,
                "expected_delivery_coefficient": expected_delivery,
                "bfv_unit_value": bfv_unit,
                "integrity_gap": integrity_gap,
                "issuable_bfv_units": nominal_units * bfv_unit,
                "escrow_retained_units": nominal_units * integrity_gap,
                "is_probabilistic_run": False
            }
        
        # --- PROBABILISTIC PATH: Full Uncertainty Error Propagation ---
        # Generate full simulation dimensions matching the maximum variable distribution length
        size = max(len(science_dist.samples), len(cobenefit_dist.samples))
        
        # Broadcast standard components out across vectors
        p_exec_vec = np.full(size, p_execution_mean)
        p_perm_vec = np.full(size, p_permanence_mean)
        p_sci_vec = np.resize(science_dist.samples, size)
        omega_vec = np.resize(cobenefit_dist.samples, size)
        
        # Element-wise product propagates variance precisely through the "weakest link" rule
        delivery_samples = p_exec_vec * p_sci_vec * p_perm_vec
        bfv_samples = delivery_samples + omega_vec
        integrity_gap_samples = np.maximum(0.0, 1.0 - bfv_samples)
        
        # Derive precise expected values from the distributions
        expected_delivery = float(np.mean(delivery_samples))
        bfv_unit = float(np.mean(bfv_samples))
        integrity_gap = float(np.mean(integrity_gap_samples))
        
        return {
            "p_execution_mean": p_execution_mean,
            "p_permanence_mean": p_permanence_mean,
            "expected_delivery_coefficient": expected_delivery,
            "bfv_unit_value": bfv_unit,
            "integrity_gap": integrity_gap,
            "issuable_bfv_units": nominal_units * bfv_unit,
            "escrow_retained_units": nominal_units * integrity_gap,
            "is_probabilistic_run": True,
            # Expose raw arrays so ledger modules can calculate arbitrary confidence intervals (e.g., VaR / 95th Percentile)
            "_raw_bfv_distribution": bfv_samples
        }
