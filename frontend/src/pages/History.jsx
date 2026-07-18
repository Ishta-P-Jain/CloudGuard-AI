import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const API_BASE_URL = "http://localhost:8000";

export default function History() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/scans`);
      if (response.ok) {
        const data = await response.json();
        setScans(data);
      }
    } catch (error) {
      console.error("Error fetching historical scans:", error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-emerald-400";
    if (score >= 50) return "text-amber-400";
    return "text-rose-400";
  };

  const formatDate = (isoString) => {
    if (!isoString) return "N/A";
    try {
      const date = new Date(isoString);
      return date.toLocaleString();
    } catch {
      return isoString;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="md:ml-56">
        <Navbar onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="px-5 py-6 md:px-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                Scan History
              </h1>
              <p className="mt-1.5 text-sm text-slate-400">
                View previous cloud audit runs and download archived PDF reports.
              </p>
            </div>
          </div>

          {loading ? (
            <div className="rounded-lg border border-slate-800 bg-slate-900 px-5 py-10 text-center text-slate-300">
              <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
                <div className="h-full w-1/3 animate-pulse rounded-full bg-cyan-400" />
              </div>
              <p className="mt-4 text-sm">Loading historical scans from the database...</p>
            </div>
          ) : scans.length === 0 ? (
            <div className="rounded-lg border border-dashed border-slate-850 bg-slate-900/50 px-5 py-16 text-center">
              <p className="text-lg font-semibold text-white">No scans found</p>
              <p className="mt-2 text-sm text-slate-400 max-w-sm mx-auto">
                No security scans have been executed yet. Go to the Dashboard and click "Run Scan" to populate this view.
              </p>
            </div>
          ) : (
            <div className="rounded-lg border border-slate-800 bg-slate-900 shadow-xl shadow-slate-950/30 overflow-x-auto">
              <table className="w-full min-w-[760px] text-left text-sm text-slate-200">
                <thead className="bg-slate-950 text-xs uppercase tracking-wide text-slate-400">
                  <tr>
                    <th className="px-5 py-3.5">Scan ID</th>
                    <th className="px-5 py-3.5">Score</th>
                    <th className="px-5 py-3.5">Critical</th>
                    <th className="px-5 py-3.5">High</th>
                    <th className="px-5 py-3.5">Medium</th>
                    <th className="px-5 py-3.5">Low</th>
                    <th className="px-5 py-3.5">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {scans.map((scan) => {
                    const summary = scan.summary || {};
                    return (
                      <tr className="hover:bg-slate-900/40 transition duration-150" key={scan.scan_id}>
                        <td className="px-5 py-4">
                          <span className="font-mono text-xs text-slate-300 block">{scan.scan_id}</span>
                        </td>
                        <td className="px-5 py-4">
                          <span className={`text-lg font-bold ${getScoreColor(scan.score)}`}>
                            {scan.score}
                          </span>
                          <span className="text-xs text-slate-400">/100</span>
                        </td>
                        <td className="px-5 py-4 font-semibold text-rose-400">{summary.critical ?? 0}</td>
                        <td className="px-5 py-4 font-semibold text-red-400">{summary.high ?? 0}</td>
                        <td className="px-5 py-4 font-semibold text-amber-400">{summary.medium ?? 0}</td>
                        <td className="px-5 py-4 font-semibold text-emerald-400">{summary.low ?? 0}</td>
                        <td className="px-5 py-4">
                          <button
                            onClick={() => window.open(`${API_BASE_URL}/api/reports/${scan.scan_id}/pdf`, "_blank")}
                            className="inline-flex items-center gap-1.5 rounded-lg border border-cyan-400/40 bg-cyan-400/10 px-3 py-1.5 text-xs font-semibold uppercase tracking-wide text-cyan-200 transition hover:bg-cyan-400/20"
                            type="button"
                          >
                            PDF Report
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
