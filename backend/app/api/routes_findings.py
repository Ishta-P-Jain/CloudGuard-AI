from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.finding import Finding
from app.schemas.finding_schema import FindingResponse

router = APIRouter(prefix="/api/scans", tags=["Findings"])

@router.get("/{scan_id}/findings", response_model=List[FindingResponse])
def get_scan_findings(scan_id: str, db: Session = Depends(get_db)):
    """
    Retrieves all security findings associated with a specific scan ID.
    """
    findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
    # Note: Even if no findings are found, returning an empty list is appropriate
    return findings
