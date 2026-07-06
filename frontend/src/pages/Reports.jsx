import Sidebar from "../components/Sidebar";

export default function Reports() {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />

      <div style={{ marginLeft: "220px", padding: "20px" }}>
        <h1>Reports</h1>
        <p>Security reports will appear here.</p>
      </div>
    </div>
  );
}