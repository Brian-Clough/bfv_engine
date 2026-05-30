from typing import List
class BetaBinomialExecutionModel:
    def __init__(self, alpha_prior: float = 2.0, beta_prior: float = 2.0):
        self.alpha_prior, self.beta_prior = alpha_prior, beta_prior
    def evaluate_posterior_mean(self, milestones: List[int]) -> float:
        if not milestones: return self.alpha_prior / (self.alpha_prior + self.beta_prior)
        successes = sum(milestones)
        alpha_post = self.alpha_prior + successes
        beta_post = self.beta_prior + (len(milestones) - successes)
        return float(alpha_post / (alpha_post + beta_post))
