import Sidebar from "../components/Sidebar";
import ScanButton from "../components/ScanButton";
import FindingsCard from "../components/FindingsCard";
import Navbar from "../components/Navbar";
import AIExplanationPanel from "../components/AIExplanationPanel";
import { checkBackendHealth } from "../api/client";
import { explainFinding } from "../api/findings";
import { getScanFindings, startScan } from "../api/scans";
import { normalizeExplanationResponse, normalizeFindingsResponse, normalizeScanResponse } from "../lib/scanData";
import { useEffect, useState } from "react";

export default function Scan() {
  const [loading, setLoading] = useState(false);
  const [findings, setFindings] = useState([]);
  const [hasScanned, setHasScanned] = useState(false);
  const [backendStatus, setBackendStatus] = useState("checking");
  const [message, setMessage] = useState("");
  const [selectedFinding, setSelectedFinding] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [explanationError, setExplanationError] = useState("");
  const [explainingFindingId, setExplainingFindingId] = useState(null);

  useEffect(() => {
    checkBackendHealth()
      .then(() => setBackendStatus("online"))
      .catch(() => setBackendStatus("offline"));
  }, []);

  const handleScan = async () => {
    setLoading(true);
    setMessage("");

    try {
      const scan = normalizeScanResponse(await startScan());
      let nextFindings = scan.findings;

      if (scan.scanId && nextFindings.length === 0) {
        nextFindings = normalizeFindingsResponse(await getScanFindings(scan.scanId));
      }

      setFindings(nextFindings);
      setHasScanned(true);
      setSelectedFinding(null);
      setExplanation(null);
      setExplanationError("");
      setBackendStatus("online");

      if (!scan.scanId && nextFindings.length === 0) {
        setMessage("The scan endpoint responded, but Student 2's full scan payload is not ready yet.");
      }
    } catch {
      setMessage("Unable to run scan. Check that the backend is running and VITE_API_BASE_URL is correct.");
      setBackendStatus("offline");
    } finally {
      setLoading(false);
    }
  };

  const handleExplainFinding = async (finding) => {
    setSelectedFinding(finding);
    setExplanation(null);
    setExplanationError("");
    setExplainingFindingId(finding.id);

    try {
      const response = await explainFinding(finding.id);
      setExplanation(normalizeExplanationResponse(response));
      setBackendStatus("online");
    } catch {
      setExplanationError("Unable to load AI explanation. Check that Student 3's Explain & Fix API is running.");
    } finally {
      setExplainingFindingId(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Sidebar />

      <div className="md:ml-56">
        <Navbar backendStatus={backendStatus} />

        <main className="px-5 py-6 md:px-8">
          <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="text-3xl font-bold">Run Cloud Scan</h1>
              <p className="mt-2 text-slate-400">
                Trigger the backend scan API and inspect the returned findings.
              </p>
            </div>
            <ScanButton onScan={handleScan} loading={loading} />
          </div>

          <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
            <FindingsCard
              explainingFindingId={explainingFindingId}
              findings={findings}
              hasScanned={hasScanned}
              loading={loading}
              message={message}
              onExplainFinding={handleExplainFinding}
              selectedFindingId={selectedFinding?.id}
            />
            <AIExplanationPanel
              error={explanationError}
              explanation={explanation}
              finding={selectedFinding}
              loading={Boolean(explainingFindingId)}
              onClose={() => {
                setSelectedFinding(null);
                setExplanation(null);
                setExplanationError("");
              }}
            />
          </div>
        </main>
      </div>
    </div>
  );
}
