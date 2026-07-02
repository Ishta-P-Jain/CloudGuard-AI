import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

function RiskChart({ findings }) {
  const count = {
    High: 0,
    Medium: 0,
    Low: 0,
  };

  findings.forEach((f) => {
    count[f.severity]++;
  });

  const data = [
    { name: "High", value: count.High },
    { name: "Medium", value: count.Medium },
    { name: "Low", value: count.Low },
  ];

  const COLORS = ["#ef4444", "#f97316", "#22c55e"];

  return (
    <div
      style={{
        background: "#111a2e",
        border: "1px solid #22304d",
        borderRadius: "16px",
        padding: "20px",
        minWidth: "320px"
      }}
    >
      <h3 style={{ color: "white" }}>RISK DISTRIBUTION</h3>

      {findings.length === 0 ? (
        <p style={{ color: "#94a3b8" }}>Run scan to see analytics</p>
      ) : (
        <PieChart width={320} height={250}>
          <Pie
            data={data}
            dataKey="value"
            outerRadius={90}
            label
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      )}
    </div>
  );
}

export default RiskChart;