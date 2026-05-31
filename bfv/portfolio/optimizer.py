import numpy as np
from typing import List, Dict, Any
from bfv.models.specs import ProjectSpecification

class BFVPortfolioOptimizer:
    """
    Implements Use Case 3 (Investor Analytics). Runs joint Monte Carlo 
    simulations over a basket of project specifications to find asset allocations 
    that maximize BFV yield while minimizing portfolio Value-at-Risk (VaR).
    """
    def __init__(self, engine):
        self.engine = engine

    def optimize_allocation(
        self, 
        project_specs: List[ProjectSpecification], 
        total_capital: float,
        risk_tolerance_alpha: float = 0.05,
        num_search_iterations: int = 1000,
        num_simulation_samples: int = 5000
    ) -> Dict[str, Any]:
        """
        Runs a probabilistic random search to trace the efficient asset frontier,
        safely handling both scalar point-estimates and sampled vector distributions.
        """
        num_assets = len(project_specs)
        if num_assets == 0:
            raise ValueError("Must provide at least one project specification.")

        # 1. Extract raw BFV simulation distributions or generate constant arrays for point-estimates
        asset_distributions = []
        for spec in project_specs:
            res = self.engine.calculate_fair_value(
                **spec.to_engine_inputs(), 
                num_simulation_samples=num_simulation_samples
            )
            
            # SAFE CHECK: If the asset returned a point estimate instead of a distribution array
            if "_raw_bfv_distribution" in res:
                dist_array = res["_raw_bfv_distribution"]
            else:
                # Expand the single unit point value into a constant vector matching our simulation shape
                dist_array = np.full(num_simulation_samples, res["bfv_unit_value"])
                
            asset_distributions.append(dist_array)
            
        # Convert to a unified matrix block [num_assets, num_simulation_samples]
        distribution_matrix = np.array(asset_distributions)
        
        best_sharpe_like_ratio = -float('inf')
        best_weights = None
        best_metrics = {}

        # 2. Search optimization loop
        for _ in range(num_search_iterations):
            raw_weights = np.random.exponential(scale=1.0, size=num_assets)
            weights = raw_weights / np.sum(raw_weights)
            
            # Compute element-wise matrix product to find portfolio returns across all rows
            portfolio_sim_returns = np.dot(weights, distribution_matrix) * total_capital
            
            # Extract key metrics
            expected_portfolio_yield = float(np.mean(portfolio_sim_returns))
            portfolio_std_dev = float(np.std(portfolio_sim_returns))
            
            # Calculate Value-at-Risk (VaR) floor
            var_floor = float(np.percentile(portfolio_sim_returns, risk_tolerance_alpha * 100))
            downside_deviation = total_capital - var_floor
            
            # Optimization Objective: Maximize yield per unit of downside risk
            risk_denominator = downside_deviation if downside_deviation > 1e-6 else 1.0
            yield_to_risk_ratio = expected_portfolio_yield / risk_denominator

            if yield_to_risk_ratio > best_sharpe_like_ratio:
                best_sharpe_like_ratio = yield_to_risk_ratio
                best_weights = weights
                best_metrics = {
                    "expected_portfolio_value_yield": expected_portfolio_yield,
                    "portfolio_standard_deviation": portfolio_std_dev,
                    "value_at_risk_floor": var_floor,
                    "downside_risk_margin": downside_deviation,
                    "yield_to_risk_ratio": yield_to_risk_ratio
                }

        # 3. Format complete output configuration sheet
        allocation_breakdown = {}
        for i, spec in enumerate(project_specs):
            allocation_breakdown[spec.project_id] = {
                "asset_type": spec.project_type,
                "weight_percentage": round(float(best_weights[i]) * 100, 2),
                "capital_allocation": round(float(best_weights[i]) * total_capital, 2)
            }

        return {
            "optimal_metrics": best_metrics,
            "portfolio_allocation_breakdown": allocation_breakdown
        }
