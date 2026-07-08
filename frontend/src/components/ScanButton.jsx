function ScanButton({ onScan, loading }) {
  return (
    <button
      onClick={onScan}
      disabled={loading}
      className="inline-flex min-h-12 items-center justify-center rounded-lg bg-cyan-400 px-6 py-3 text-sm font-bold uppercase tracking-wide text-slate-950 shadow-lg shadow-cyan-950/30 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:bg-slate-600 disabled:text-slate-300"
    >
      {loading ? "Scanning..." : "Run New Cloud Scan"}
    </button>
  );
}

export default ScanButton;
