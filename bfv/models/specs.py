from dataclasses import dataclass, field
from typing import List, Dict, Any, Union

@dataclass
class ProjectSpecification:
    """
    Hardened input boundary contract for a BFV carbon asset pipeline entry.
    Decouples core cookie-cutter metrics from highly project-specific variables.
    """
    project_id: str
    project_type: str                  # e.g., 'Industrial IFM', 'Frontier OAE', 'DAC'
    nominal_units: float               # P, total nominal credit tons under valuation
    
    # Built-In Cookie-Cutter Risk Vectors
    execution_milestones: List[int]     # Binary history (1=achieved, 0=delayed)
    historical_reversal_rate_100yr: float # Baseline Weibull hazard probability
    k_shape: float                      # Risk trajectory profile curve over time
    
    # Externalized Project-Specific Vectors
    # Supports scalar float point-estimates, parameter dicts, or MCMC lists/arrays
    science_risk: Union[float, Dict[str, float], List[float]]
    co_benefits: Union[float, Dict[str, float], List[float]]
    
    # Metadata anchor for passing auxiliary unstructured field records
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_engine_inputs(self) -> Dict[str, Any]:
        """
        Transforms the project spec into the exact dictionary keyword inputs 
        demanded by the BFVEngine calculation interface.
        """
        return {
            "milestones": self.execution_milestones,
            "science_input": self.science_risk,
            "historical_reversal_rate_100yr": self.historical_reversal_rate_100yr,
            "k_shape": self.k_shape,
            "co_benefit_input": self.co_benefits,
            "nominal_units": self.nominal_units
        }
