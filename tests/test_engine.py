import unittest
import numpy as np
from bfv.statistics.execution import BetaBinomialExecutionModel
from bfv.statistics.permanence import WeibullPermanenceModel
from bfv.statistics.engine import BFVEngine
from bfv.models.specs import ProjectSpecification

class TestBFVCorePlatform(unittest.TestCase):
    def setUp(self):
        self.exec_model = BetaBinomialExecutionModel(alpha_prior=2.0, beta_prior=2.0)
        self.perm_model = WeibullPermanenceModel(target_years=1000.0)
        self.engine = BFVEngine(execution_model=self.exec_model, permanence_model=self.perm_model)

    def test_zero_reversal_permanence_boundary(self):
        """Ensure that a zero-reversal rate maps accurately to a perfect 1.0 permanence score."""
        p_perm = self.perm_model.calculate_survival_probability(historical_reversal_rate_100yr=0.0, k_shape=1.0)
        self.assertEqual(p_perm, 1.0)

    def test_complete_reversal_permanence_boundary(self):
        """Ensure that 100% near-term depletion drops 1000-year survival to absolute 0.0."""
        p_perm = self.perm_model.calculate_survival_probability(historical_reversal_rate_100yr=1.0, k_shape=1.0)
        self.assertEqual(p_perm, 0.0)

    def test_execution_prior_with_empty_milestones(self):
        """Ensure that empty historical profiles fall back cleanly onto the standard 50/50 prior mean."""
        p_exec = self.exec_model.evaluate_posterior_mean([])
        self.assertEqual(p_exec, 0.5)

    def test_engine_fast_path_scalar_execution(self):
        """Validate that passing standard scalars returns a flat point-estimate calculation pass."""
        res = self.engine.calculate_fair_value(
            milestones=[1, 1, 1],
            science_input=0.90,
            historical_reversal_rate_100yr=0.05,
            k_shape=1.0,
            co_benefit_input=0.02,
            nominal_units=1000.0
        )
        self.assertFalse(res["is_probabilistic_run"])
        self.assertIn("bfv_unit_value", res)
        # Total accounted asset capacity must equal nominal units exactly
        self.assertAlmostEqual(res["issuable_bfv_units"] + res["escrow_retained_units"], 1000.0)

if __name__ == '__main__':
    unittest.main()
