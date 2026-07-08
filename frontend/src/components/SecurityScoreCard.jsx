function SecurityScoreCard({ score }) {
  let risk = "LOW RISK";
  let color = "text-emerald-300";
  let ring = "from-emerald-500/20";

  if (score < 80) {
    risk = "MODERATE RISK";
    color = "text-amber-300";
    ring = "from-amber-500/20";
  }

  if (score < 50) {
    risk = "HIGH RISK";
    color = "text-rose-300";
    ring = "from-rose-500/20";
  }

  return (
    <div className={`rounded-lg border border-slate-800 bg-gradient-to-br ${ring} to-slate-900 p-6 shadow-xl shadow-slate-950/30`}>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
        Security Risk Score
      </h3>

      <div className="mt-5 flex items-end gap-2">
        <h1 className={`text-6xl font-bold leading-none ${color}`}>
        {score}
      </h1>
        <p className="pb-2 text-lg text-slate-400">/ 100</p>
      </div>

      <h2 className={`mt-4 text-sm font-bold uppercase tracking-wide ${color}`}>{risk}</h2>
    </div>
  );
}

export default SecurityScoreCard;
