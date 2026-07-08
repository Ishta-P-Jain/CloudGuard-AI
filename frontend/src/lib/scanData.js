export function normalizeSeverity(value) {
  const severity = String(value || "low").toLowerCase();

  if (severity === "critical") return "Critical";
  if (severity === "high") return "High";
  if (severity === "medium") return "Medium";
  if (severity === "low") return "Low";

  return "Low";
}

export function normalizeScanResponse(scan) {
  const summary = scan?.summary || {};

  return {
    scanId: scan?.scan_id || scan?.id || null,
    status: scan?.status || "completed",
    score: Number(scan?.score ?? scan?.security_score ?? 0),
    summary: {
      total: Number(summary.total ?? scan?.total_findings ?? 0),
      critical: Number(summary.critical ?? scan?.critical_count ?? 0),
      high: Number(summary.high ?? scan?.high_count ?? 0),
      medium: Number(summary.medium ?? scan?.medium_count ?? 0),
      low: Number(summary.low ?? scan?.low_count ?? 0),
    },
    findings: Array.isArray(scan?.findings) ? scan.findings.map(normalizeFinding) : [],
  };
}

export function normalizeFindingsResponse(response) {
  const list = Array.isArray(response) ? response : response?.findings || [];
  return list.map(normalizeFinding);
}

export function normalizeFinding(finding) {
  return {
    id: finding.id || finding.finding_id || finding.resource_id || crypto.randomUUID(),
    service: finding.service || finding.cloud_service || "Cloud",
    resourceId: finding.resource_id || finding.resource || "Unknown resource",
    title: finding.title || finding.rule_name || "Security finding",
    severity: normalizeSeverity(finding.severity || finding.risk),
    description: finding.description || finding.message || "No description provided.",
  };
}

export function buildSummary(findings) {
  return findings.reduce(
    (summary, finding) => {
      const key = normalizeSeverity(finding.severity).toLowerCase();
      summary.total += 1;
      summary[key] += 1;
      return summary;
    },
    { total: 0, critical: 0, high: 0, medium: 0, low: 0 },
  );
}

