# BFV Engine Framework (Bayesian Fair Value)

A high-utility Python platform implementing the **Bayesian Fair Value (BFV) Framework** for risk-adjusted climate finance. This package quantifies asset delivery probabilities by modeling joint posterior distribution overlaps across three critical dimensions: Execution, Scientific Measurement, and 1,000-Year Structural Permanence.

\[BFV = (P 	imes E[\Theta]) + \Omega\]

---

## 🌟 The Three Operational Personas

This framework serves three distinct industry workflows:

### 📊 1. The Rating Engine (Single Project Analytics)
Evaluates an isolated project specification. It accepts raw point estimates, parametric inputs, or MCMC chain simulation traces to perform multi-variable Monte Carlo error propagation and output standard deviation bounds.

### 🏛️ 2. The Registry Ledger Stack (Dynamic Uncertainty Banking)
Orchestrates a three-tiered systemic credit reserve system. Automates credit value releases or emergency clawbacks into project escrows (Layer 1), central repository pools (Layer 2), or external insurance backstops (Layer 3) based on active monitoring updates.

### 📈 3. The Investor Portfolio Optimizer
Applies modern portfolio allocation concepts directly to asymmetrical carbon risk curves. Utilizes matrix-accelerated random searches to find asset splits that maximize forward expected BFV yield while minimizing portfolio-wide downside Value-at-Risk (VaR).

---

## 🚀 Quick Start Example

```python
import numpy as np
from bfv.statistics.execution import BetaBinomialExecutionModel
from bfv.statistics.permanence import WeibullPermanenceModel
from bfv.statistics.engine import BFVEngine
from bfv.models.specs import ProjectSpecification
from bfv.portfolio.optimizer import BFVPortfolioOptimizer

# 1. Initialize Math Core
engine = BFVEngine(
    execution_model=BetaBinomialExecutionModel(),
    permanence_model=WeibullPermanenceModel()
)

# 2. Structure a Project Specification Input Contract
spec = ProjectSpecification(
    project_id="forestry-project-alpha",
    project_type="Industrial IFM",
    nominal_units=5000.0,
    execution_milestones=[1]*18 + [0]*2,
    historical_reversal_rate_100yr={"mean": 0.04, "variance": 0.002},
    k_shape=1.4,
    science_risk=0.92,
    co_benefits=0.05
)

# 3. Compute BFV Rating
metrics = engine.calculate_fair_value(**spec.to_engine_inputs())
print(f"Risk-Adjusted BFV Unit Value: {metrics['bfv_unit_value']:.4f}")
```

---

## 🧪 Running the Test Suite

Validate mathematical boundaries and file configurations using standard package discovery:
```bash
python -m unittest discover -s tests
```
