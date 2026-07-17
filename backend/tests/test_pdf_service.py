from types import SimpleNamespace

from app.services.pdf_service import build_scan_pdf


def test_build_scan_pdf_returns_pdf_bytes():
    scan = SimpleNamespace(
        id="scan-1",
        status="completed",
        score=82,
        total_findings=2,
    )

    findings = [
        SimpleNamespace(
            service="EC2",
            severity="HIGH",
            title="Open SSH",
            ai_explanation=SimpleNamespace(explanation="SSH is open to the internet."),
        ),
        SimpleNamespace(
            service="S3",
            severity="MEDIUM",
            title="Public Bucket",
            ai_explanation=None,
        ),
    ]

    buffer = build_scan_pdf(scan, findings)
    pdf_bytes = buffer.getvalue()

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes[:4] == b"%PDF"


def test_build_scan_pdf_handles_missing_ai_explanation():
    scan = SimpleNamespace(
        id="scan-2",
        status="completed",
        score=91,
        total_findings=1,
    )

    findings = [
        SimpleNamespace(
            service="EC2",
            severity="LOW",
            title="Safe Instance",
            ai_explanation=None,
        ),
    ]

    buffer = build_scan_pdf(scan, findings)

    assert buffer.getbuffer().nbytes > 0
