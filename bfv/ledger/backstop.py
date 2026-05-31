from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Dict, Any

@dataclass
class CapitalInjectionRecord:
    injection_id: str
    provider_name: str         # e.g., 'Sovereign Buffer Fund', 'Munich Re'
    amount: float
    timestamp: str
    injection_type: str        # e.g., 'EQUITY', 'REINSURANCE_DRAW', 'GRANT'

class InsuranceBackstop:
    """
    Implements Layer 3 Insurance Backstop mechanics. Manages external 
    macro-capital injections when Layer 1 and Layer 2 buffers face depletion.
    """
    def __init__(self, backstop_id: str):
        self.backstop_id = backstop_id
        self.available_capital = 0.0
        self.injections: List[CapitalInjectionRecord] = []
        self.injection_counter = 0

    def inject_external_capital(self, provider: str, amount: float, injection_type: str = "REINSURANCE_DRAW"):
        """Logs an external capital injection to strengthen the sovereign systemic buffer."""
        if amount <= 0:
            raise ValueError("Injection amount must be positive.")
            
        self.available_capital += amount
        self.injection_counter += 1
        injection_id = f"INJ-{self.injection_counter:04d}"
        
        self.injections.append(CapitalInjectionRecord(
            injection_id=injection_id,
            provider_name=provider,
            amount=amount,
            timestamp=datetime.now(timezone.utc).isoformat(),
            injection_type=injection_type
        ))
        return injection_id

    def draw_down_backstop(self, amount: float) -> float:
        """Draws emergency liquidity out of the Layer 3 fund to rescue lower layers."""
        if amount > self.available_capital:
            drawn = self.available_capital
            self.available_capital = 0.0
        else:
            drawn = amount
            self.available_capital -= amount
        return drawn

    def get_backstop_status(self) -> Dict[str, Any]:
        return {
            "backstop_id": self.backstop_id,
            "available_backstop_capital": round(self.available_capital, 2),
            "total_injections_logged": len(self.injections)
        }
