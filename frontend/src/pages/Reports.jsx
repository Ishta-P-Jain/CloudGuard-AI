import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import ReportDownloadButton from "../components/ReportDownloadButton";
import { getLatestScan, getScanFindings } from "../api/scans";
import { checkBackendHealth } from "../api/client";
import { normalizeScanResponse, normalizeFindingsResponse } from "../lib/scanData";
import { FileText, ShieldAlert, ArrowRight, ShieldCheck } from "lucide-react";


export default function Reports() {
  const [latestScan, setLatestScan] = useState(null);
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [backendStatus, setBackendStatus] = useState("checking");

  useEffect(() => {
    checkBackendHealth()
      .then(() => setBackendStatus("online"))
      .catch(() => setBackendStatus("offline"));

    const fetchLatestReport = async () => {
      try {
        const rawScan = await getLatestScan();
        const scan = normalizeScanResponse(rawScan);
        setLatestScan(scan);

        if (scan.scanId) {
          const rawFindings = await getScanFindings(scan.scanId);
          setFindings(normalizeFindingsResponse(rawFindings));
        }
      } catch (error) {
        console.warn("No scan records or backend is offline:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchLatestReport();
  }, []);

  return (
    <Layout backendStatus={backendStatus}>
      <div className="mb-6">
        <h1 className="text-2xl font-bold md:text-3xl">Security Reports</h1>
        <p className="mt-1 text-sm text-slate-400">
          Access and download security compliance reports for your cloud infrastructure scans.
        </p>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-slate-800 bg-slate-900/50">
          <div className="flex flex-col items-center gap-3">
            <span className="h-8 w-8 animate-spin rounded-full border-4 border-cyan-400 border-t-transparent" />
            <p className="text-sm text-slate-400">Loading latest scan reports...</p>
          </div>
        </div>
      ) : latestScan ? (
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Main Report Details Card */}
          <div className="lg:col-span-2 rounded-lg border border-slate-800 bg-slate-900 p-6 shadow-xl">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-cyan-500/10 p-3 text-cyan-400 border border-cyan-500/20">
                  <FileText className="h-6 w-6" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-white">Latest Security Assessment</h2>
                  <p className="text-xs font-mono text-slate-500 mt-0.5">Scan ID: {latestScan.scanId}</p>
                </div>
              </div>
              <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${
                latestScan.score >= 80 
                  ? "border-emerald-400/40 bg-emerald-500/15 text-emerald-200" 
                  : latestScan.score >= 50
                  ? "border-amber-400/40 bg-amber-500/15 text-amber-200"
                  : "border-rose-400/40 bg-rose-500/15 text-rose-200"
              }`}>
                Score: {latestScan.score}/100
              </span>
            </div>

            <div className="mt-6 border-t border-slate-800 pt-6">
              <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300">Scan Summary</h3>
              <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
                <div className="rounded-lg bg-slate-950/60 p-3 text-center border border-slate-800/40">
                  <p className="text-xs text-slate-500">Critical</p>
                  <p className="mt-1 text-lg font-bold text-rose-400">{latestScan.summary.critical}</p>
                </div>
                <div className="rounded-lg bg-slate-950/60 p-3 text-center border border-slate-800/40">
                  <p className="text-xs text-slate-500">High</p>
                  <p className="mt-1 text-lg font-bold text-red-400">{latestScan.summary.high}</p>
                </div>
                <div className="rounded-lg bg-slate-950/60 p-3 text-center border border-slate-800/40">
                  <p className="text-xs text-slate-500">Medium</p>
                  <p className="mt-1 text-lg font-bold text-amber-400">{latestScan.summary.medium}</p>
                </div>
                <div className="rounded-lg bg-slate-950/60 p-3 text-center border border-slate-800/40">
                  <p className="text-xs text-slate-500">Low</p>
                  <p className="mt-1 text-lg font-bold text-emerald-400">{latestScan.summary.low}</p>
                </div>
              </div>
            </div>

            <div className="mt-8 flex items-center justify-between border-t border-slate-800 pt-6">
              <span className="text-xs text-slate-500">
                Generated PDF includes all security issues and remediation steps.
              </span>
              <ReportDownloadButton 
                findings={findings} 
                scanId={latestScan.scanId} 
                score={latestScan.score} 
              />
            </div>
          </div>

          {/* Quick Stats & Recommendations Side Card */}
          <div className="rounded-lg border border-slate-800 bg-slate-900 p-6 flex flex-col justify-between">
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300 mb-4">
                Assessment Insights
              </h3>
              {latestScan.score === 100 ? (
                <div className="flex items-start gap-3 rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-4">
                  <ShieldCheck className="h-5 w-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-semibold text-emerald-200">Excellent Security Posture</h4>
                    <p className="mt-1 text-xs text-emerald-400/80 leading-relaxed">
                      No security issues detected. Your cloud resource configurations align with standard best practices.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="flex items-start gap-3 rounded-lg border border-amber-500/20 bg-amber-500/5 p-4">
                  <ShieldAlert className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-semibold text-amber-200">Action Required</h4>
                    <p className="mt-1 text-xs text-amber-400/80 leading-relaxed">
                      Your score is {latestScan.score}/100. Fix the {latestScan.summary.critical + latestScan.summary.high} critical and high severity findings to improve resilience.
                    </p>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-6 border-t border-slate-800 pt-6">
              <Link
                to="/scan"
                className="flex w-full items-center justify-between rounded-lg border border-slate-800 bg-slate-950/40 px-4 py-3 text-sm text-slate-300 transition hover:bg-slate-950 hover:text-white"
              >
                <span>Run a fresh security scan</span>
                <ArrowRight className="h-4 w-4 text-cyan-400" />
              </Link>
            </div>
          </div>
        </div>
      ) : (
        <div className="rounded-lg border border-dashed border-slate-800 bg-slate-900/20 p-12 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-slate-900 border border-slate-800 text-slate-500 mb-4">
            <ShieldAlert className="h-6 w-6" />
          </div>
          <h2 className="text-lg font-bold text-white">No Reports Found</h2>
          <p className="mt-2 text-sm text-slate-400 max-w-md mx-auto">
            You must run a security scan first before we can compile your audit logs and generate PDF reports.
          </p>
          <div className="mt-6">
            <Link
              to="/scan"
              className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
            >
              <span>Go to Scan</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      )}
    </Layout>
  );
}
