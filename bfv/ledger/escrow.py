class ProjectEscrowLedger:
    def __init__(self, project_id, nominal_units):
        self.project_id, self.nominal_units = project_id, nominal_units
        self.circulating_balance, self.escrow_balance, self.history = 0.0, 0.0, []
    def initialize_allocation(self, engine_results):
        self.circulating_balance = engine_results["issuable_bfv_units"]
        self.escrow_balance = engine_results["escrow_retained_units"]
    def reconcile_state(self, engine_results, event_name="RECONCILE"):
        self.circulating_balance = engine_results["issuable_bfv_units"]
        self.escrow_balance = engine_results["escrow_retained_units"]
    def get_summary(self):
        return {"project_id": self.project_id, "nominal_pool": self.nominal_units, "circulating_balance": round(self.circulating_balance, 2), "escrow_balance": round(self.escrow_balance, 2)}
