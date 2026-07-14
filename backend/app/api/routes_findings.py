from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.database import get_db
from app.models.finding import Finding
from app.models.ai_explanation import AIExplanation
from app.models.usage_limit import UsageLimit
from app.schemas.finding_schema import FindingResponse
from app.schemas.ai_schema import AIExplanationResponse
from app.services.ai_service import explain_finding

router = APIRouter(tags=["Findings"])

@router.get("/api/scans/{scan_id}/findings", response_model=List[FindingResponse])
def get_scan_findings(scan_id: str, db: Session = Depends(get_db)):
    """
    Retrieves all security findings associated with a specific scan ID.
    """
    findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
    return findings

@router.post("/api/findings/{finding_id}/explain", response_model=AIExplanationResponse)
def get_finding_explanation(finding_id: str, db: Session = Depends(get_db)):
    """
    Generates or retrieves a cached AI-powered explanation and remediation plan for a finding.
    Implements database caching and daily cost usage limits.
    """
    # 1. Caching check: if explanation already exists, return it immediately
    cached_explanation = db.query(AIExplanation).filter(AIExplanation.finding_id == finding_id).first()
    if cached_explanation:
        print(f"[Findings Router] Serving explanation for finding {finding_id} from database cache.")
        return cached_explanation

    # 2. Daily Cost Usage Limit Check:
    today = date.today()
    usage = db.query(UsageLimit).filter(UsageLimit.date == today).first()
    if not usage:
        usage = UsageLimit(date=today, request_count=0)
        db.add(usage)
        db.flush()

    if usage.request_count >= 50:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily AI explanation limit of 50 requests reached. Please try again tomorrow."
        )

    # 3. Retrieve finding details from DB
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finding record not found."
        )

    # 4. Generate AI explanation using the ai_service
    finding_dict = {
        "service": finding.service,
        "rule_id": finding.rule_id,
        "resource_id": finding.resource_id,
        "severity": finding.severity,
        "description": finding.description,
        "evidence": finding.evidence
    }
    
    explanation_data = explain_finding(finding_dict)

    # 5. Persist explanation to database cache & update parent finding
    try:
        new_explanation = AIExplanation(
            finding_id=finding_id,
            explanation=explanation_data["explanation"],
            danger=explanation_data["danger"],
            real_world_impact=explanation_data["real_world_impact"],
            remediation_steps=explanation_data["remediation_steps"],
            estimated_effort=explanation_data["estimated_effort"]
        )
        db.add(new_explanation)
        
        # Mark parent finding as explained
        finding.has_ai_explanation = True
        
        # Increment daily usage count
        usage.request_count += 1
        
        db.commit()
        db.refresh(new_explanation)
        
        return new_explanation
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process and cache the explanation: {str(e)}"
        )
