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