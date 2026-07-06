import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import SecurityScoreCard from "../components/SecurityScoreCard";
import VulnerabilityCard from "../components/VulnerabilityCard";
import RiskSummaryCard from "../components/RiskSummaryCard";
import ScanButton from "../components/ScanButton";
import FindingsCard from "../components/FindingsCard";
import { useState } from "react";

export default function Dashboard() {
  const [score, setScore] = useState(82);
  const [loading, setLoading] = useState(false);
  const [findings, setFindings] = useState([]);

  const runScan = () => {
    setLoading(true);

    setTimeout(() => {
      setScore(74);
      setFindings([
        { id: 1, title: "Open Port Detected", severity: "High", description: "Port 22 is open to 0.0.0.0/0" },
        { id: 2, title: "Weak Password", severity: "Medium", description: "Password complexity is not enforced" },
        { id: 3, title: "Outdated Package", severity: "Low", description: "Vulnerable libraries are in use" },
      ]);
      setLoading(false);
    }, 1500);
  };

  const calculateStats = (findingsList) => {
    const stats = { high: 0, medium: 0, low: 0 };
    findingsList.forEach((f) => {
      const severity = (f.risk || f.severity || "").toLowerCase();
      if (severity === "high") {
        stats.high++;
      } else if (severity === "medium") {
        stats.medium++;
      } else if (severity === "low") {
        stats.low++;
      }
    });
    return stats;
  };

  const stats = calculateStats(findings);

  return (
    <div style={styles.wrapper}>
      <Sidebar />

      <div style={styles.main}>
        <Navbar />

        <h1 style={styles.title}>Security Dashboard</h1>

        <div style={styles.grid}>
          <SecurityScoreCard score={score} />
          <VulnerabilityCard stats={stats} />
          <RiskSummaryCard findings={findings} />
        </div>

        <ScanButton onScan={runScan} loading={loading} />

        <FindingsCard findings={findings} loading={loading} />
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    background: "#0b1220",
    color: "white",
    minHeight: "100vh",
  },

  main: {
    marginLeft: "220px",
    width: "100%",
    padding: "20px",
  },

  title: {
    fontSize: "28px",
    margin: "10px 0 20px",
  },

  grid: {
    display: "flex",
    gap: "15px",
    flexWrap: "wrap",
  },
};