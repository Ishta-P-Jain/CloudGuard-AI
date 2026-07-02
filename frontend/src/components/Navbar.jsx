function Navbar() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "20px 30px",
        background: "#081120",
        borderBottom: "1px solid #22304d"
      }}
    >
      <div>
        <h1 style={{ margin: 0, color: "white", fontSize: "32px" }}>
          CLOUDGUARD AI
        </h1>
        <p style={{ margin: 0, color: "#9ca3af" }}>
          SECURITY AUDIT DASHBOARD
        </p>
      </div>

      <div style={{ display: "flex", gap: "15px" }}>
        <div
          style={{
            background: "#14532d",
            padding: "10px 14px",
            borderRadius: "10px",
            color: "#86efac"
          }}
        >
          Backend Status: Online
        </div>

        <div
          style={{
            background: "#1e3a8a",
            padding: "10px 14px",
            borderRadius: "10px",
            color: "#93c5fd"
          }}
        >
          LocalStack: Running
        </div>
      </div>
    </div>
  );
}

export default Navbar;