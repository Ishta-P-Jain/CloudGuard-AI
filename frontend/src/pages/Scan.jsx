import Sidebar from "../components/Sidebar";
import ScanButton from "../components/ScanButton";
import FindingsCard from "../components/FindingsCard";
import { useState } from "react";

export default function Scan() {
  const [loading, setLoading] = useState(false);
  const [findings, setFindings] = useState([]);

  const startScan = () => {
    setLoading(true);

    setTimeout(() => {
      setFindings([
        { id: 1, title: "Open Port Detected", severity: "High", description: "Port 22 is open to 0.0.0.0/0" },
        { id: 2, title: "Weak Password", severity: "Medium", description: "Password complexity is not enforced" },
      ]);
      setLoading(false);
    }, 1500);
  };

  return (
    <div style={{ display: "flex" }}>
      <Sidebar />

      <div style={{ marginLeft: "220px", padding: "20px" }}>
        <h1>Scan Page</h1>

        <ScanButton onScan={startScan} loading={loading} />
        <FindingsCard findings={findings} loading={loading} />
      </div>
    </div>
  );
}