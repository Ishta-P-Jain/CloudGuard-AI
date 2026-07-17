from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.finding import Finding
from app.models.scan import Scan
from app.services.pdf_service import build_scan_pdf

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/{scan_id}/pdf")
def download_scan_report(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found.",
        )

    from sqlalchemy.orm import joinedload
    findings = db.query(Finding).options(joinedload(Finding.ai_explanation)).filter(Finding.scan_id == scan_id).all()
    pdf_buffer = build_scan_pdf(scan, findings)
    filename = f"cloudguard_scan_{scan_id}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
