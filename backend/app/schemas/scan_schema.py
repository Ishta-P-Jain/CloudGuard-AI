from pydantic import BaseModel
from typing import Dict

class ScanSummary(BaseModel):
    total: int
    critical: int
    high: int
    medium: int
    low: int

class ScanResponse(BaseModel):
    scan_id: str
    status: str
    score: int
    summary: ScanSummary

    class Config:
        from_attributes = True
