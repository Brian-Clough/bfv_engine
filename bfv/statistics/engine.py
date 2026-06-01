import numpy as np
from bfv.statistics.inputs import ProbabilisticInput
class BFVEngine:
    def __init__(self, execution_model, permanence_model):
        self.execution_model, self.permanence_model = execution_model, permanence_model
    def calculate_fair_value(self, milestones, science_input, historical_reversal_rate_100yr, k_shape, co_benefit_input, nominal_units=1.0, num_simulation_samples=2000):
        science_dist = ProbabilisticInput(science_input, num_samples=num_simulation_samples)
        reversal_dist = ProbabilisticInput(historical_reversal_rate_100yr, num_samples=num_simulation_samples)
        cobenefit_dist = ProbabilisticInput(co_benefit_input, num_samples=num_simulation_samples)
        p_exec_mean = self.execution_model.evaluate_posterior_mean(milestones)
        if science_dist.is_point_estimate and reversal_dist.is_point_estimate and cobenefit_dist.is_point_estimate:
            p_perm_mean = self.permanence_model.calculate_survival_probability(reversal_dist.evaluate_mean(), k_shape)
            expected_delivery = float(p_exec_mean * science_dist.evaluate_mean() * p_perm_mean)
            bfv_unit = float(expected_delivery + cobenefit_dist.evaluate_mean())
            integrity_gap = max(0.0, 1.0 - bfv_unit)
            return {"p_execution_mean": p_exec_mean, "p_permanence_mean": p_perm_mean, "expected_delivery_coefficient": expected_delivery, "bfv_unit_value": bfv_unit, "integrity_gap": integrity_gap, "issuable_bfv_units": nominal_units * bfv_unit, "escrow_retained_units": nominal_units * integrity_gap}
        p_exec_samples = np.random.beta(self.execution_model.alpha_prior + sum(milestones), self.execution_model.beta_prior + len(milestones) - sum(milestones), size=num_simulation_samples)
        p_perm_samples = np.array([self.permanence_model.calculate_survival_probability(r, k_shape) for r in reversal_dist.samples])
        p_perm_samples = np.resize(p_perm_samples, num_simulation_samples)
        p_sci_samples = np.resize(science_dist.samples, num_simulation_samples)
        omega_samples = np.resize(cobenefit_dist.samples, num_simulation_samples)
        delivery_samples = p_exec_samples * p_sci_samples * p_perm_samples
        bfv_samples = delivery_samples + omega_samples
        integrity_gap_samples = np.maximum(0.0, 1.0 - bfv_samples)
        return {"p_execution_mean": float(np.mean(p_exec_samples)), "p_permanence_mean": float(np.mean(p_perm_samples)), "expected_delivery_coefficient": float(np.mean(delivery_samples)), "bfv_unit_value": float(np.mean(bfv_samples)), "integrity_gap": float(np.mean(integrity_gap_samples)), "issuable_bfv_units": nominal_units * float(np.mean(bfv_samples)), "escrow_retained_units": nominal_units * float(np.mean(integrity_gap_samples)), "bfv_standard_deviation": float(np.std(bfv_samples)), "bfv_5th_percentile": float(np.percentile(bfv_samples, 5)), "bfv_95th_percentile": float(np.percentile(bfv_samples, 95)), "_raw_bfv_distribution": bfv_samples}
