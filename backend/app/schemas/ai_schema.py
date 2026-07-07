from pydantic import BaseModel
from typing import List

class AIExplanationResponse(BaseModel):
    explanation: str
    danger: str
    real_world_impact: str
    remediation_steps: List[str]
    estimated_effort: str

    class Config:
        from_attributes = True
