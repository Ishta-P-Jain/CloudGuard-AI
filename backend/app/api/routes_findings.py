from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ai_explanation import AIExplanation
from app.models.finding import Finding
from app.models.usage_limit import UsageLimit
from app.schemas.ai_schema import AIExplanationResponse
from app.schemas.finding_schema import FindingResponse
from app.services.ai_service import generate_ai_explanation

router = APIRouter(prefix="/api/scans", tags=["Findings"])

MAX_DAILY_AI_REQUESTS = 100


@router.get("/{scan_id}/findings", response_model=List[FindingResponse])
def get_scan_findings(scan_id: str, db: Session = Depends(get_db)):
    """
    Retrieves all security findings associated with a specific scan ID.
    """
    findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
    return findings


@router.post(
    "/{scan_id}/findings/{finding_id}/explanation",
    response_model=AIExplanationResponse,
    status_code=status.HTTP_201_CREATED,
)
def explain_finding(scan_id: str, finding_id: str, db: Session = Depends(get_db)):
    """
    Returns a cached AI explanation if one already exists.
    Otherwise it generates a fresh explanation, saves it, and returns it.
    """
    finding = (
        db.query(Finding)
        .filter(Finding.scan_id == scan_id, Finding.id == finding_id)
        .first()
    )
    if not finding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finding not found for this scan.",
        )

    cached = db.query(AIExplanation).filter(AIExplanation.finding_id == finding.id).first()
    if cached:
        return {
            "explanation": cached.explanation,
            "danger": cached.danger,
            "real_world_impact": cached.real_world_impact,
            "remediation_steps": cached.remediation_steps,
            "estimated_effort": cached.estimated_effort,
        }

    usage = db.query(UsageLimit).filter(UsageLimit.date == date.today()).first()
    if usage and usage.request_count >= MAX_DAILY_AI_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily AI request limit reached.",
        )

    if not usage:
        usage = UsageLimit(date=date.today(), request_count=0)
        db.add(usage)
        db.flush()

    payload = generate_ai_explanation(
        {
            "service": finding.service,
            "resource_id": finding.resource_id,
            "title": finding.title,
            "severity": finding.severity,
            "description": finding.description,
            "evidence": finding.evidence or {},
            "rule_id": finding.title,
        }
    )

    ai_row = AIExplanation(
        finding_id=finding.id,
        explanation=payload["explanation"],
        danger=payload["danger"],
        real_world_impact=payload["real_world_impact"],
        remediation_steps=payload["remediation_steps"],
        estimated_effort=payload["estimated_effort"],
    )

    finding.has_ai_explanation = True
    finding.ai_explanation = ai_row
    usage.request_count += 1

    db.add(ai_row)
    db.commit()
    db.refresh(ai_row)

    return payload