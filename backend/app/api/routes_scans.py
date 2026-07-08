from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.scan import Scan
from app.models.finding import Finding
from app.schemas.scan_schema import ScanResponse
from app.services.scanner_service import scan_localstack
from app.services.risk_service import calculate_score

router = APIRouter(prefix="/api/scans", tags=["Scans"])

@router.post("", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
def run_new_scan(db: Session = Depends(get_db)):
    """
    Triggers a security scan against LocalStack, evaluates risk scores, 
    persists scan results & findings to PostgreSQL, and returns a scan summary.
    """
    try:
        # 1. Run localstack scanner
        raw_findings = scan_localstack()
        
        # 2. Calculate risk score and finding summary stats
        risk_metrics = calculate_score(raw_findings)
        score = risk_metrics["score"]
        summary = risk_metrics["summary"]
        
        # 3. Persist the main Scan record
        new_scan = Scan(
            status="completed",
            score=score,
            total_findings=summary["total"],
            critical_count=summary["critical"],
            high_count=summary["high"],
            medium_count=summary["medium"],
            low_count=summary["low"]
        )
        db.add(new_scan)
        db.flush()  # flush to generate new_scan.id
        
        # 4. Persist findings associated with this scan
        for raw in raw_findings:
            new_finding = Finding(
                scan_id=new_scan.id,
                service=raw.get("service", "Unknown"),
                resource_id=raw.get("resource_id", "Unknown"),
                title=raw.get("title", "No Title"),
                severity=raw.get("severity", "LOW").upper(),
                description=raw.get("description", ""),
                evidence=raw.get("evidence", {}),
                has_ai_explanation=False
            )
            db.add(new_finding)
            
        db.commit()
        db.refresh(new_scan)
        
        # 5. Map to response format
        return {
            "scan_id": new_scan.id,
            "status": new_scan.status,
            "score": new_scan.score,
            "summary": {
                "total": new_scan.total_findings,
                "critical": new_scan.critical_count,
                "high": new_scan.high_count,
                "medium": new_scan.medium_count,
                "low": new_scan.low_count
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during the scan operation: {str(e)}"
        )

@router.get("/latest", response_model=ScanResponse)
def get_latest_scan(db: Session = Depends(get_db)):
    """
    Retrieves the most recent security scan summary.
    """
    latest_scan = db.query(Scan).order_by(Scan.created_at.desc()).first()
    if not latest_scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scan records found in the database. Run a scan first."
        )
        
    return {
        "scan_id": latest_scan.id,
        "status": latest_scan.status,
        "score": latest_scan.score,
        "summary": {
            "total": latest_scan.total_findings,
            "critical": latest_scan.critical_count,
            "high": latest_scan.high_count,
            "medium": latest_scan.medium_count,
            "low": latest_scan.low_count
        }
    }
