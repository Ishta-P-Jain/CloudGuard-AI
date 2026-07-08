import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function Reports() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Sidebar />

      <div className="md:ml-56">
        <Navbar backendStatus="checking" />
        <main className="px-5 py-6 md:px-8">
          <h1 className="text-3xl font-bold">Reports</h1>
          <p className="mt-2 text-slate-400">Security reports will appear here.</p>
        </main>
      </div>
    </div>
  );
}
