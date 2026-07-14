const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Downloads a security report as a PDF.
 * Attempts to hit the backend endpoint GET /api/reports/{scan_id}/pdf.
 * If it fails or is not implemented, falls back to generating a valid PDF locally in the client.
 * 
 * @param {string} scanId - The ID of the scan
 * @param {Array} findings - The findings to include if generating client-side fallback PDF
 * @param {number} score - The security score to show in the report
 */
export async function downloadReportPdf(scanId, findings = [], score = 100) {
  if (!scanId) {
    throw new Error("No scan ID provided for report download.");
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/reports/${scanId}/pdf`, {
      method: "GET",
    });

    if (response.ok) {
      const blob = await response.blob();
      triggerDownload(blob, `cloudguard-security-report-${scanId.slice(0, 8)}.pdf`);
      return { success: true, fallback: false };
    }
  } catch (err) {
    console.warn("Backend PDF download failed or was unavailable, using client-side fallback PDF generation:", err);
  }

  // Client-side fallback PDF generation
  const pdfBlob = generateClientPdf(scanId, findings, score);
  triggerDownload(pdfBlob, `cloudguard-security-report-fallback-${scanId.slice(0, 8)}.pdf`);
  return { success: true, fallback: true };
}

function triggerDownload(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

/**
 * Generates a basic PDF document structure client-side.
 * Uses standard PDF-1.4 format syntax to create a single-page document.
 */
function generateClientPdf(scanId, findings, score) {
  const title = "CloudGuard AI Security Audit Report";
  const dateStr = new Date().toLocaleString();
  const summaryText = `Scan ID: ${scanId}\\nDate: ${dateStr}\\nSecurity Score: ${score}/100\\nTotal Findings: ${findings.length}`;

  let findingsText = "";
  findings.forEach((f, idx) => {
    findingsText += `\\n${idx + 1}. [${f.severity || "LOW"}] ${f.title || "Finding"} (${f.service || "Cloud"}) - ${f.resourceId || "Unknown"}\\n   Description: ${f.description || "No description."}\\n`;
  });

  // Clean strings for PDF compatibility
  const cleanTitle = title.replace(/[()]/g, "");
  const cleanSummary = summaryText.replace(/[()]/g, "\\$&");
  const cleanFindings = findingsText.replace(/[()]/g, "\\$&");

  const pdfBody = `BT
/F1 18 Tf
50 780 Td
(${cleanTitle}) Tj
/F1 11 Tf
0 -30 Td
(${cleanSummary.replace(/\\n/g, ") Tj 0 -15 Td (")}) Tj
0 -40 Td
(Security Findings Details:) Tj
/F1 9 Tf
0 -20 Td
(${cleanFindings.replace(/\\n/g, ") Tj 0 -13 Td (")}) Tj
ET`;

  const pdfContent = `%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /Contents 4 0 R >>
endobj
4 0 obj
<< /Length ${pdfBody.length} >>
stream
${pdfBody}
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000281 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
${281 + 45 + pdfBody.length + 15}
%%EOF`;

  return new Blob([pdfContent], { type: "application/pdf" });
}
