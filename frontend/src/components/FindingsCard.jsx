function SeverityBadge({ severity }) {
  const classes = {
    Critical: "border-rose-400/40 bg-rose-500/15 text-rose-100",
    High: "border-red-400/40 bg-red-500/15 text-red-100",
    Medium: "border-amber-400/40 bg-amber-500/15 text-amber-100",
    Low: "border-emerald-400/40 bg-emerald-500/15 text-emerald-100",
  };

  return (
    <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${classes[severity] || classes.Low}`}>
      {severity}
    </span>
  );
}

function FindingsCard({ findings, loading, hasScanned, message }) {
  return (
    <div className="mt-6 rounded-lg border border-slate-800 bg-slate-900 shadow-xl shadow-slate-950/30">
      <div className="border-b border-slate-800 px-5 py-4">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
          Security Findings
        </h3>
        {message && <p className="mt-2 text-sm text-amber-100">{message}</p>}
      </div>

      {loading ? (
        <div className="px-5 py-10 text-slate-300">
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
            <div className="h-full w-1/2 animate-pulse rounded-full bg-cyan-400" />
          </div>
          <p className="mt-4 text-sm">Scanning cloud resources and loading findings...</p>
        </div>
      ) : findings.length === 0 ? (
        <div className="px-5 py-10 text-center">
          <p className="text-lg font-semibold text-white">
            {hasScanned ? "No findings found" : "No scan run yet"}
          </p>
          <p className="mt-2 text-sm text-slate-400">
            {hasScanned
              ? "The latest scan did not return any security findings."
              : "Run a cloud scan to populate this table with backend results."}
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-left text-sm text-slate-200">
            <thead className="bg-slate-950 text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-5 py-3">Finding</th>
                <th className="px-5 py-3">Severity</th>
                <th className="px-5 py-3">Service</th>
                <th className="px-5 py-3">Resource</th>
                <th className="px-5 py-3">Description</th>
              </tr>
            </thead>

            <tbody>
              {findings.map((item) => (
                <tr className="border-t border-slate-800" key={item.id}>
                  <td className="px-5 py-4 font-medium text-white">{item.title}</td>
                  <td className="px-5 py-4"><SeverityBadge severity={item.severity} /></td>
                  <td className="px-5 py-4">{item.service}</td>
                  <td className="px-5 py-4 font-mono text-xs text-slate-300">{item.resourceId}</td>
                  <td className="px-5 py-4 text-slate-300">{item.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default FindingsCard;
