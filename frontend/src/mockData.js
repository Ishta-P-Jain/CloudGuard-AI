export const mockScanData = {
  score: 82,
  totalFindings: 12,

  vulnerabilities: [
    {
      id: 1,
      title: "Outdated dependency detected",
      severity: "High"
    },
    {
      id: 2,
      title: "Weak password policy",
      severity: "Medium"
    },
    {
      id: 3,
      title: "Missing security headers",
      severity: "Low"
    }
  ],

  lastScanned: "2026-06-30 10:30 AM"
};