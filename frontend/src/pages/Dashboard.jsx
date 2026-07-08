import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import SecurityScoreCard from "../components/SecurityScoreCard";
import VulnerabilityCard from "../components/VulnerabilityCard";
import RiskSummaryCard from "../components/RiskSummaryCard";
import ScanButton from "../components/ScanButton";
import FindingsCard from "../components/FindingsCard";
import RiskChart from "../components/RiskChart";
import { checkBackendHealth } from "../api/client";
import { getScanFindings, startScan } from "../api/scans";
import { buildSummary, normalizeFindingsResponse, normalizeScanResponse } from "../lib/scanData";
import { useEffect, useMemo, useState } from "react";

export default function Dashboard() {
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(false);
  const [findings, setFindings] = useState([]);
  const [hasScanned, setHasScanned] = useState(false);
  const [backendStatus, setBackendStatus] = useState("checking");
  const [message, setMessage] = useState("");

  useEffect(() => {
    checkBackendHealth()
      .then(() => setBackendStatus("online"))
      .catch(() => setBackendStatus("offline"));
  }, []);

  const runScan = async () => {
    setLoading(true);
    setMessage("");

    try {
      const scan = normalizeScanResponse(await startScan());
      let nextFindings = scan.findings;

      if (scan.scanId && nextFindings.length === 0) {
        nextFindings = normalizeFindingsResponse(await getScanFindings(scan.scanId));
      }

      const summary = nextFindings.length > 0 ? buildSummary(nextFindings) : scan.summary;

      setScore(scan.score);
      setFindings(nextFindings);
      setHasScanned(true);
      setBackendStatus("online");

      if (!scan.scanId && nextFindings.length === 0) {
        setMessage("The scan endpoint responded, but Student 2's full scan payload is not ready yet.");
      } else if (summary.total === 0) {
        setMessage("Scan completed successfully with no findings.");
      }
    } catch {
      setMessage("Unable to run scan. Check that the backend is running and VITE_API_BASE_URL is correct.");
      setBackendStatus("offline");
    } finally {
      setLoading(false);
    }
  };

  const stats = useMemo(() => buildSummary(findings), [findings]);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Sidebar />

      <div className="md:ml-56">
        <Navbar backendStatus={backendStatus} />

        <main className="px-5 py-6 md:px-8">
          <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h1 className="text-3xl font-bold">Security Dashboard</h1>
              <p className="mt-2 text-slate-400">
                Run a backend scan and review the latest cloud security findings.
              </p>
            </div>
            <ScanButton onScan={runScan} loading={loading} />
          </div>

          <div className="grid gap-4 lg:grid-cols-4">
            <SecurityScoreCard score={score} />
            <VulnerabilityCard stats={stats} />
            <RiskSummaryCard summary={stats} />
            <RiskChart findings={findings} />
          </div>

          <FindingsCard
            findings={findings}
            hasScanned={hasScanned}
            loading={loading}
            message={message}
          />
        </main>
      </div>
    </div>
  );
}
