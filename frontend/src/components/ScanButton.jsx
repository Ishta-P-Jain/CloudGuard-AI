function ScanButton({ onScan, loading }) {
  return (
    <button
      onClick={onScan}
      disabled={loading}
      style={{
        padding: "16px 28px",
        background: "linear-gradient(90deg, #4f46e5, #ec4899)",
        border: "none",
        borderRadius: "12px",
        color: "white",
        fontWeight: "bold",
        fontSize: "16px",
        cursor: "pointer"
      }}
    >
      {loading ? "Scanning..." : "RUN NEW CLOUD SCAN"}
    </button>
  );
}

export default ScanButton;