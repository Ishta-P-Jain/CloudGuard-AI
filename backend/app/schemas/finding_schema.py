from pydantic import BaseModel

class FindingResponse(BaseModel):
    id: str
    rule_id: str
    service: str
    resource_id: str
    title: str
    severity: str
    description: str
    has_ai_explanation: bool

    class Config:
        from_attributes = True
