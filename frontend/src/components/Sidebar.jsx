import { Link, useLocation } from "react-router-dom";
import { X, LayoutDashboard, ShieldAlert, FileBarChart2, History } from "lucide-react";

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/", icon: LayoutDashboard },
    { name: "Scan", path: "/scan", icon: ShieldAlert },
    { name: "Reports", path: "/reports", icon: FileBarChart2 },
    { name: "History", path: "/history", icon: History },
  ];

  return (
    <>
      {/* Mobile Overlay backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-950/80 backdrop-blur-sm transition-opacity duration-300 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar container */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-56 flex-col border-r border-slate-800 bg-slate-950 px-5 py-6 text-white transition-transform duration-300 md:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } md:flex`}
      >
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-500/20 text-cyan-400 font-bold border border-cyan-500/30">
              CG
            </span>
            <h2 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              CloudGuard
            </h2>
          </div>
          {/* Close button for mobile */}
          <button
            className="rounded-lg border border-slate-800 p-1.5 text-slate-400 hover:bg-slate-900 hover:text-white md:hidden"
            onClick={onClose}
            type="button"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <nav className="flex flex-col gap-1.5 text-sm">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 font-medium transition duration-200 ${
                  isActive
                    ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
                    : "text-slate-400 border border-transparent hover:bg-slate-900 hover:text-slate-200"
                }`}
                key={item.path}
                onClick={onClose}
                to={item.path}
              >
                <Icon className={`h-4 w-4 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

      </aside>
    </>
  );
}
