function SecurityScoreCard({ score }) {
  let risk = "LOW RISK";
  let color = "#22c55e";

  if (score < 80) {
    risk = "MODERATE RISK";
    color = "#f59e0b";
  }

  if (score < 50) {
    risk = "HIGH RISK";
    color = "#ef4444";
  }

  return (
    <div
      style={{
        background: "#111a2e",
        border: "1px solid #22304d",
        borderRadius: "16px",
        padding: "25px",
        minWidth: "300px",
        boxShadow: "0 0 20px rgba(0,0,0,0.3)"
      }}
    >
      <h3 style={{ color: "white" }}>SECURITY RISK SCORE</h3>

      <h1
        style={{
          fontSize: "72px",
          margin: "20px 0 10px 0",
          color: color
        }}
      >
        {score}
      </h1>

      <p style={{ color: "#94a3b8", fontSize: "20px" }}>/ 100</p>

      <h2 style={{ color: color }}>{risk}</h2>
    </div>
  );
}

export default SecurityScoreCard;