import { apiRequest } from "./client";

export async function explainFinding(findingId) {
  return apiRequest(`/api/findings/${findingId}/explain`, { method: "POST" });
}

