import numpy as np

class WeibullPermanenceModel:
    """
    Implements a Weibull Survival Hazard model for carbon asset permanence.
    """
    def __init__(self, target_years: float = 1000.0):
        self.target_years = target_years

    def calculate_survival_probability(self, historical_reversal_rate_100yr: float, k_shape: float) -> float:
        # High-permanence boundary fallback: If there is zero risk, permanence is absolute
        if historical_reversal_rate_100yr <= 0.0:
            return 1.0
            
        survival_100 = 1.0 - historical_reversal_rate_100yr
        
        # Risk depletion fallback: If 100% of assets reverse in 100 years, 1000-year survival is impossible
        if survival_100 <= 0.0:
            return 0.0
            
        # Calibrate scale parameter (lambda) using the 100-year boundary profile
        lambda_scale = ((-np.log(survival_100)) ** (1.0 / k_shape)) / 100.0
        
        # Evaluate terminal target horizon survival
        p_permanence = np.exp(-(lambda_scale * self.target_years) ** k_shape)
        
        return float(p_permanence)
