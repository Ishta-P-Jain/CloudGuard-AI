import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 hidden w-56 flex-col border-r border-slate-800 bg-slate-950 px-5 py-6 text-white md:flex">
      <h2 className="mb-8 text-xl font-bold">CloudGuard</h2>

      <nav className="flex flex-col gap-2 text-sm">
        <Link className="rounded-lg px-3 py-2 text-slate-300 hover:bg-slate-800 hover:text-white" to="/">
          Dashboard
        </Link>
        <Link className="rounded-lg px-3 py-2 text-slate-300 hover:bg-slate-800 hover:text-white" to="/scan">
          Scan
        </Link>
        <Link className="rounded-lg px-3 py-2 text-slate-300 hover:bg-slate-800 hover:text-white" to="/reports">
          Reports
        </Link>
      </nav>
    </aside>
  );
}
