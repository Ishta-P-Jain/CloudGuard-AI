import { Menu } from "lucide-react";

function Navbar({ backendStatus = "checking", onMenuToggle }) {
  const statusStyles = {
    online: "border-emerald-500/30 bg-emerald-500/10 text-emerald-200",
    offline: "border-rose-500/30 bg-rose-500/10 text-rose-200",
    checking: "border-amber-500/30 bg-amber-500/10 text-amber-100",
  };

  return (
    <div className="flex flex-col gap-4 border-b border-slate-800 bg-slate-950/80 px-5 py-4 md:flex-row md:items-center md:justify-between md:px-8">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Hamburger Menu Trigger for Mobile */}
          <button
            className="rounded-lg border border-slate-800 p-2 text-slate-400 hover:bg-slate-900 hover:text-white md:hidden"
            onClick={onMenuToggle}
            type="button"
          >
            <Menu className="h-5 w-5" />
          </button>

          <div>
            <h1 className="text-xl font-bold text-white md:text-2xl">CloudGuard AI</h1>
            <p className="text-xs uppercase tracking-wide text-slate-400">
              Security Audit Dashboard
            </p>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 text-xs md:text-sm">
        <div className={`rounded-lg border px-3 py-1.5 ${statusStyles[backendStatus] || statusStyles.checking}`}>
          Backend: {backendStatus}
        </div>
        <div className="rounded-lg border border-sky-500/30 bg-sky-500/10 px-3 py-1.5 text-sky-200">
          LocalStack Ready
        </div>
      </div>
    </div>
  );
}

export default Navbar;
