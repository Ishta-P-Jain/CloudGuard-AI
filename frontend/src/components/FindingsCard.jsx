function FindingsCard({ findings, loading }) {
  return (
    <div
      style={{
        background: "#111a2e",
        border: "1px solid #22304d",
        borderRadius: "16px",
        padding: "20px",
        marginTop: "20px"
      }}
    >
      <h3 style={{ color: "white" }}>SECURITY FINDINGS TABLE</h3>

      {loading ? (
        <p style={{ color: "#94a3b8" }}>Scanning...</p>
      ) : findings.length === 0 ? (
        <p style={{ color: "#94a3b8" }}>No scan run yet.</p>
      ) : (
        <table style={{ width: "100%", marginTop: "20px", color: "white" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Finding</th>
              <th>Severity</th>
              <th>Description</th>
            </tr>
          </thead>

          <tbody>
            {findings.map((item, index) => (
              <tr key={item.id}>
                <td>{index + 1}</td>
                <td>{item.title}</td>
                <td>{item.severity}</td>
                <td>{item.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default FindingsCard;