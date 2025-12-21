from dataclasses import dataclass
from typing import List, Optional

@dataclass
class InsuranceInputs:
    age: int
    annual_income: float
    dependents: int
    existing_life_cover: float
    existing_health_cover: float

    city_tier: str                      
    lifestyle_risks: Optional[List[str]] = None
