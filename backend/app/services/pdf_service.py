from io import BytesIO
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend

from app.models.finding import Finding
from app.models.scan import Scan
from app.services.report_service import build_fallback_remediation


def build_scan_pdf(scan: Scan, findings: List[Finding]) -> BytesIO:
    buffer = BytesIO()
    
    # 1. Document template setup (0.75-inch margins, printable width is 504 pt)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        title=f"CloudGuard AI Scan {scan.id}",
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )
    
    body_cell_style = ParagraphStyle(
        'BodyCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )
    
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,  # Centered
        spaceAfter=15
    )
    
    meta_style = ParagraphStyle(
        'ReportMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#475569")
    )

    elements = []
    
    # Header Section
    elements.append(Paragraph("CloudGuard AI Security Report", title_style))
    elements.append(Paragraph(f"<b>Scan ID:</b> {scan.id}", meta_style))
    elements.append(Paragraph(f"<b>Status:</b> {scan.status}", meta_style))
    elements.append(Paragraph(f"<b>Score:</b> {scan.score}", meta_style))
    elements.append(Paragraph(f"<b>Total Findings:</b> {scan.total_findings}", meta_style))
    elements.append(Spacer(1, 15))

    # --- EXECUTIVE SCORE SUMMARY CARD ---
    if scan.score >= 80:
        score_color = '#10b981'  # Emerald 500
        risk_label = "LOW RISK"
    elif scan.score >= 50:
        score_color = '#f59e0b'  # Amber 500
        risk_label = "MODERATE RISK"
    else:
        score_color = '#ef4444'  # Red 500
        risk_label = "HIGH RISK"
        
    score_html = f"<font size=32 color='{score_color}'><b>{scan.score}</b></font><font size=14 color='#64748b'> / 100</font>"
    score_para = Paragraph(score_html, styles['Normal'])
    risk_para = Paragraph(f"<font size=13 color='{score_color}'><b>{risk_label}</b></font>", styles['Normal'])
    
    # Calculate findings breakdown for summary
    summary_count = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for f in findings:
        sev = f.severity.capitalize()
        if sev in summary_count:
            summary_count[sev] += 1
        else:
            summary_count["Low"] += 1

    sev_text = f"""
    <b>Summary Breakdown:</b><br/>
    <font color='#f43f5e'>• Critical: {summary_count['Critical']}</font> &nbsp;&nbsp;
    <font color='#ef4444'>• High: {summary_count['High']}</font> &nbsp;&nbsp;
    <font color='#f59e0b'>• Medium: {summary_count['Medium']}</font> &nbsp;&nbsp;
    <font color='#10b981'>• Low: {summary_count['Low']}</font>
    """
    sev_para = Paragraph(sev_text, body_cell_style)
    
    score_data = [
        [score_para, sev_para],
        [risk_para, ""]
    ]
    score_table = Table(score_data, colWidths=[180, doc.width - 180])
    score_table.setStyle(TableStyle([
        ('SPAN', (0, 1), (0, 1)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(score_table)
    elements.append(Spacer(1, 15))

    # --- RISK DISTRIBUTION CHART (PIE CHART) ---
    chart_data = []
    chart_labels = []
    chart_colors = []
    
    color_map = {
        "Critical": colors.HexColor("#fb7185"),  # Pink 400 (matches chart frontend)
        "High": colors.HexColor("#f87171"),      # Red 400
        "Medium": colors.HexColor("#f59e0b"),    # Amber 500
        "Low": colors.HexColor("#34d399")        # Emerald 400
    }
    
    for category in ["Critical", "High", "Medium", "Low"]:
        val = summary_count[category]
        if val > 0:
            chart_data.append(val)
            chart_labels.append(f"{category} ({val})")
            chart_colors.append(color_map[category])
            
    if chart_data:
        chart_title_style = ParagraphStyle(
            'ChartTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#475569"),
            spaceAfter=6,
            keepWithNext=True
        )
        elements.append(Paragraph("Risk Distribution Analysis", chart_title_style))
        
        drawing = Drawing(doc.width, 130)
        pc = Pie()
        pc.x = 80
        pc.y = 5
        pc.width = 120
        pc.height = 120
        pc.data = chart_data
        pc.labels = []  # Hide labels on pie slices to use clean legend
        
        # Color configuration for pie slices
        for idx_slice, color in enumerate(chart_colors):
            pc.slices[idx_slice].fillColor = color
            
        drawing.add(pc)
        
        # Add Legend to the right of the Pie chart
        legend = Legend()
        legend.x = 260
        legend.y = 100
        legend.dx = 8
        legend.dy = 8
        legend.dxTextSpace = 6
        legend.yGap = 8
        legend.fontName = 'Helvetica'
        legend.fontSize = 8.5
        legend.boxAnchor = 'nw'
        legend.columnMaximum = 4
        legend.colorNamePairs = [(chart_colors[i], chart_labels[i]) for i in range(len(chart_data))]
        drawing.add(legend)
        
        elements.append(drawing)
        elements.append(Spacer(1, 15))

    # --- DETAILED FINDINGS TABLE ---
    # Table Header Row
    headers = [
        Paragraph("Service", header_cell_style),
        Paragraph("Severity", header_cell_style),
        Paragraph("Title", header_cell_style),
        Paragraph("AI / Fallback Summary", header_cell_style)
    ]
    rows = [headers]
    
    # Table Body Rows
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
                Paragraph(finding.service, body_cell_style),
                Paragraph(finding.severity, body_cell_style),
                Paragraph(finding.title, body_cell_style),
                Paragraph(summary_text, body_cell_style),
            ]
        )

    # Column widths summing up exactly to doc.width (504 pt)
    col_widths = [60, 54, 160, 230]
    
    table = Table(rows, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e2937")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer