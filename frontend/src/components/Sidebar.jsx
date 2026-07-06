import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div style={styles.sidebar}>
      <h2>CloudGuard</h2>

      <Link to="/">Dashboard</Link>
      <Link to="/scan">Scan</Link>
      <Link to="/reports">Reports</Link>
    </div>
  );
}

const styles = {
  sidebar: {
    width: "200px",
    height: "100vh",
    background: "#111827",
    color: "white",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "15px",
    position: "fixed",
  },
};