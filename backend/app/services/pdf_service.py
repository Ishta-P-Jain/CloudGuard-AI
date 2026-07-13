from io import BytesIO
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models.finding import Finding
from app.models.scan import Scan
from app.services.report_service import build_fallback_remediation


def build_scan_pdf(scan: Scan, findings: List[Finding]) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=f"CloudGuard AI Scan {scan.id}")
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("CloudGuard AI Security Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Scan ID: {scan.id}", styles["Normal"]))
    elements.append(Paragraph(f"Status: {scan.status}", styles["Normal"]))
    elements.append(Paragraph(f"Score: {scan.score}", styles["Normal"]))
    elements.append(Paragraph(f"Total Findings: {scan.total_findings}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    rows = [["Service", "Severity", "Title", "AI / Fallback Summary"]]
    for finding in findings:
        explanation = getattr(finding, "ai_explanation", None)
        if explanation:
            summary_text = explanation.explanation
        else:
            fallback = build_fallback_remediation(
                {
                    "service": finding.service,
                    "title": finding.title,
                    "rule_id": finding.title,
                }
            )
            summary_text = fallback["explanation"]

        rows.append(
            [
                finding.service,
                finding.severity,
                finding.title,
                summary_text,
            ]
        )

    table = Table(rows, colWidths=[80, 60, 160, 220])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer