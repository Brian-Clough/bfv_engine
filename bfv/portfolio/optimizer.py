import numpy as np
class BFVPortfolioOptimizer:
    def __init__(self, engine): self.engine = engine
    def optimize_allocation(self, project_specs, total_budget, project_prices, num_search_iterations=500):
        num_assets = len(project_specs)
        asset_unit_distributions = []
        for spec in project_specs:
            res = self.engine.calculate_fair_value(**spec.to_engine_inputs(), num_simulation_samples=1000)
            dist_array = res.get("_raw_bfv_distribution", np.full(1000, res["bfv_unit_value"]))
            asset_unit_distributions.append(dist_array)
        distribution_matrix = np.array(asset_unit_distributions)
        prices = np.array([project_prices[spec.project_id] for spec in project_specs])
        best_ratio, best_weights = -float('inf'), None
        for _ in range(num_search_iterations):
            w = np.random.exponential(scale=1.0, size=num_assets); w /= np.sum(w)
            purchased_nominal_tons = (w * total_budget) / prices
            portfolio_sim_returns = np.dot(purchased_nominal_tons, distribution_matrix)
            exp_yield = float(np.mean(portfolio_sim_returns))
            var_floor = float(np.percentile(portfolio_sim_returns, 5))
            downside = np.sum(purchased_nominal_tons) - var_floor
            ratio = exp_yield / (downside if downside > 1e-6 else 1.0)
            if ratio > best_ratio: best_ratio, best_weights = ratio, w
        breakdown = {}
        for i, spec in enumerate(project_specs):
            breakdown[spec.project_id] = {"asset_type": spec.project_type, "budget_weight_percentage": round(float(best_weights[i]) * 100, 2), "capital_allocated_dollars": round(float(best_weights[i]) * total_budget, 2)}
        return {"portfolio_allocation_breakdown": breakdown}
