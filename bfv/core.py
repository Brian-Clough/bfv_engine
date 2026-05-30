from typing import Dict, Any

class BaseBFVAsset:
    def __init__(self, name: str, nominal_tons: float, omega: float = 0.0):
        self.name = name
        self.nominal_tons = nominal_tons
        self.omega = omega
        self.e_theta = 1.0

    def calculate_bfv(self, p_e: float, p_s: float, p_p: float) -> Dict[str, Any]:
        self.e_theta = p_e * p_s * p_p
        bfv_val = max(0.0, self.e_theta + self.omega)
        return {
            "Asset": self.name,
            "E[Theta]": round(self.e_theta, 3),
            "BFV Value": round(bfv_val, 3)
        }
