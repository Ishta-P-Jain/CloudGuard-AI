function RiskSummaryCards({ summary }) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-6 shadow-xl shadow-slate-950/30">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
        Total Findings
      </h2>

      <div className="mt-5">
        <p className="text-5xl font-bold text-white">{summary.total}</p>
        <p className="mt-2 text-sm text-slate-400">
          {summary.total === 0 ? "No active findings from the latest scan." : "Findings detected in the latest scan."}
        </p>
      </div>
    </div>
  );
}

export default RiskSummaryCards;
