from typing import List
class BetaBinomialExecutionModel:
    def __init__(self, alpha_prior=2.0, beta_prior=2.0):
        self.alpha_prior, self.beta_prior = alpha_prior, beta_prior
    def evaluate_posterior_mean(self, milestones: List[int]) -> float:
        if not milestones: return self.alpha_prior / (self.alpha_prior + self.beta_prior)
        successes = sum(milestones)
        return float((self.alpha_prior + successes) / (self.alpha_prior + self.beta_prior + len(milestones)))
