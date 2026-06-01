from dataclasses import dataclass
@dataclass
class ProjectSpecification:
    project_id: str; project_type: str; nominal_units: float; execution_milestones: list; historical_reversal_rate_100yr: float; k_shape: float; science_risk: float; co_benefits: float
    def to_engine_inputs(self):
        return {"milestones": self.execution_milestones, "science_input": self.science_risk, "historical_reversal_rate_100yr": self.historical_reversal_rate_100yr, "k_shape": self.k_shape, "co_benefit_input": self.co_benefits, "nominal_units": self.nominal_units}
