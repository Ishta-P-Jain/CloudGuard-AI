import Layout from "../components/Layout";
import ScanButton from "../components/ScanButton";
import FindingsCard from "../components/FindingsCard";
import AIExplanationPanel from "../components/AIExplanationPanel";
import ReportDownloadButton from "../components/ReportDownloadButton";
import { checkBackendHealth } from "../api/client";
import { explainFinding } from "../api/findings";
import { getScanFindings, startScan } from "../api/scans";
import { normalizeExplanationResponse, normalizeFindingsResponse, normalizeScanResponse } from "../lib/scanData";
import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";

export default function Scan() {
  const [scanId, setScanId] = useState(null);
  const [score, setScore] = useState(100); // Default score or calculate dynamically
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
    const toastId = toast.loading("Initiating cloud security scan...");

    try {
      const scan = normalizeScanResponse(await startScan());
      let nextFindings = scan.findings;

      if (scan.scanId && nextFindings.length === 0) {
        nextFindings = normalizeFindingsResponse(await getScanFindings(scan.scanId));
      }

      setScanId(scan.scanId);
      setScore(scan.score);
      setFindings(nextFindings);
      setHasScanned(true);
      setSelectedFinding(null);
      setExplanation(null);
      setExplanationError("");
      setBackendStatus("online");

      if (!scan.scanId && nextFindings.length === 0) {
        setMessage("The scan endpoint responded, but Student 2's full scan payload is not ready yet.");
        toast.error("Scan finished, but payload is incomplete.", { id: toastId });
      } else {
        toast.success(`Scan completed successfully! Found ${nextFindings.length} findings.`, {
          id: toastId,
          duration: 4000,
        });
      }
    } catch (err) {
      console.error(err);
      setMessage("Unable to run scan. Check that the backend is running and VITE_API_BASE_URL is correct.");
      setBackendStatus("offline");
      toast.error("Scan failed. Backend is offline or unreachable.", { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  const handleExplainFinding = async (finding) => {
    setSelectedFinding(finding);
    setExplanation(null);
    setExplanationError("");
    setExplainingFindingId(finding.id);
    const toastId = toast.loading(`Requesting AI explanation for "${finding.title}"...`);

    try {
      const response = await explainFinding(finding.id);
      setExplanation(normalizeExplanationResponse(response));
      setBackendStatus("online");
      toast.success("AI analysis loaded successfully!", { id: toastId });
    } catch (err) {
      console.error(err);
      setExplanationError("Unable to load AI explanation. Check that Student 3's Explain & Fix API is running.");
      toast.error("Failed to load AI explanation.", { id: toastId });
    } finally {
      setExplainingFindingId(null);
    }
  };

  return (
    <Layout backendStatus={backendStatus}>
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold md:text-3xl">Run Cloud Scan</h1>
          <p className="mt-1 text-sm text-slate-400">
            Trigger the backend scan API and inspect the returned findings.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {hasScanned && (
            <ReportDownloadButton
              findings={findings}
              scanId={scanId}
              score={score}
            />
          )}
          <ScanButton loading={loading} onScan={handleScan} />
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
        <div className="overflow-hidden">
          <FindingsCard
            explainingFindingId={explainingFindingId}
            findings={findings}
            hasScanned={hasScanned}
            loading={loading}
            message={message}
            onExplainFinding={handleExplainFinding}
            selectedFindingId={selectedFinding?.id}
          />
        </div>
        <div className="xl:sticky xl:top-6">
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
      </div>
    </Layout>
  );
}
