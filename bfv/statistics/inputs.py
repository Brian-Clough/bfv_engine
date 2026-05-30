import numpy as np
from typing import Union, Dict, Any, List

class ProbabilisticInput:
    """
    Polymorphic wrapper that translates scalars, parametric distributions, 
    or MCMC chain samples into standard Monte Carlo simulation arrays.
    """
    def __init__(self, data: Any, num_samples: int = 5000):
        self.num_samples = num_samples
        self.samples = self._parse_input(data)

    def _parse_input(self, data: Any) -> np.ndarray:
        # Form 1: Raw Point Estimate (Scalar)
        if isinstance(data, (int, float)):
            return np.array([float(data)])

        # Form 2: Array or List of MCMC Posterior Samples
        if isinstance(data, (list, np.ndarray)):
            return np.atleast_1d(np.array(data, dtype=float))

        # Form 3: Mean & Variance Parameterized Map
        if isinstance(data, dict) and "mean" in data and "variance" in data:
            mu = float(data["mean"])
            var = float(data["variance"])
            
            # For edge boundary edge cases with zero uncertainty, fallback to point estimate
            if var <= 0:
                return np.array([mu])
                
            # If values fall within [0, 1] probability range, fit an analytical Beta distribution
            if 0 < mu < 1 and var < (mu * (1 - mu)):
                # Method of moments conversion to find alpha and beta parameters
                nu = mu * (1 - mu) / var - 1
                alpha = mu * nu
                beta = (1 - mu) * nu
                return np.random.beta(alpha, beta, size=self.num_samples)
                
            # Generic unconstrained fallback using Gaussian distributions
            return np.random.normal(mu, np.sqrt(var), size=self.num_samples)

        raise ValueError(f"Unsupported ProbabilisticInput format: {type(data)}")

    @property
    def is_point_estimate(self) -> bool:
        """Flag to tell the engine if it can skip expensive vector loops."""
        return len(self.samples) == 1

    def evaluate_mean(self) -> float:
        """Extracts a traditional point estimate expected mean value."""
        return float(np.mean(self.samples))
