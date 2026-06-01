import numpy as np
class ProbabilisticInput:
    def __init__(self, data, num_samples=5000):
        self.num_samples = num_samples
        self.samples = self._parse_input(data)
    def _parse_input(self, data):
        if isinstance(data, (int, float)): return np.array([float(data)])
        if isinstance(data, (list, np.ndarray)): return np.atleast_1d(np.array(data, dtype=float))
        if isinstance(data, dict) and "mean" in data and "variance" in data:
            mu, var = float(data["mean"]), float(data["variance"])
            if var <= 0: return np.array([mu])
            if 0 < mu < 1 and var < (mu * (1 - mu)):
                nu = mu * (1 - mu) / var - 1
                return np.random.beta(mu * nu, (1 - mu) * nu, size=self.num_samples)
            return np.random.normal(mu, np.sqrt(var), size=self.num_samples)
        raise ValueError(f"Unsupported format: {type(data)}")
    @property
    def is_point_estimate(self): return len(self.samples) == 1
    def evaluate_mean(self): return float(np.mean(self.samples))
