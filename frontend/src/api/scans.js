import { apiRequest } from "./client";

export async function startScan() {
  return apiRequest("/api/scans", { method: "POST" });
}

export async function getLatestScan() {
  return apiRequest("/api/scans/latest");
}

export async function getScanFindings(scanId) {
  return apiRequest(`/api/scans/${scanId}/findings`);
}

