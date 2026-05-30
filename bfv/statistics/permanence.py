import numpy as np
class WeibullPermanenceModel:
    def __init__(self, target_years: float = 1000.0): self.target_years = target_years
    def calculate_survival_probability(self, historical_reversal_rate_100yr: float, k_shape: float) -> float:
        survival_100 = 1.0 - historical_reversal_rate_100yr
        if survival_100 <= 0 or survival_100 >= 1: return 0.0
        lambda_scale = ((-np.log(survival_100)) ** (1.0 / k_shape)) / 100.0
        return float(np.exp(-(lambda_scale * self.target_years) ** k_shape))
