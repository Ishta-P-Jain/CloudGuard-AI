import Navbar from "../components/Navbar";
import SecurityScoreCard from "../components/SecurityScoreCard";
import VulnerabilityCard from "../components/VulnerabilityCard";
import RiskChart from "../components/RiskChart";
import ScanButton from "../components/ScanButton";
import FindingsCard from "../components/FindingsCard";
import { useState } from "react";

function Dashboard() {
  const [score, setScore] = useState(0);
  const [vulnStats, setVulnStats] = useState({ critical: 0, high: 0, medium: 0, low: 0 });
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateScanResults = async () => {
    setLoading(true);
    try {
      // Add API call here to fetch scan results
      const response = await fetch('/api/scan');
      const data = await response.json();
      setFindings(data.findings);
      setScore(data.score);
      setVulnStats(data.stats);
    } catch (error) {
      console.error("Error generating scan results:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
  <div style={{ background: "#081120", minHeight: "100vh", color: "white" }}>
    <Navbar />

  <div style={{ padding: "20px" }}>
    
    <div
      style={{
        display: "flex",
        gap: "20px",
        flexWrap: "wrap",
        alignItems: "flex-start"
      }}
    >
      <SecurityScoreCard score={score} />
      <VulnerabilityCard stats={vulnStats} />
      <RiskChart findings={findings} />
    </div>

    <div style={{ marginTop: "20px" }}>
      <ScanButton onScan={generateScanResults} loading={loading} />
    </div>

    <FindingsCard findings={findings} loading={loading} />
  </div>
</div>
);
}
export default Dashboard;
    