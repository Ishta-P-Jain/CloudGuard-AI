function Navbar({ backendStatus = "checking" }) {
  const statusStyles = {
    online: "border-emerald-500/30 bg-emerald-500/10 text-emerald-200",
    offline: "border-rose-500/30 bg-rose-500/10 text-rose-200",
    checking: "border-amber-500/30 bg-amber-500/10 text-amber-100",
  };

  return (
    <div className="flex flex-col gap-4 border-b border-slate-800 bg-slate-950/80 px-5 py-5 md:flex-row md:items-center md:justify-between md:px-8">
      <div>
        <h1 className="text-2xl font-bold text-white md:text-3xl">CloudGuard AI</h1>
        <p className="text-sm uppercase tracking-wide text-slate-400">
          Security Audit Dashboard
        </p>
      </div>

      <div className="flex flex-wrap gap-3 text-sm">
        <div className={`rounded-lg border px-3 py-2 ${statusStyles[backendStatus]}`}>
          Backend: {backendStatus}
        </div>
        <div className="rounded-lg border border-sky-500/30 bg-sky-500/10 px-3 py-2 text-sky-200">
          LocalStack Ready
        </div>
      </div>
    </div>
  );
}

export default Navbar;
