import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { normalizeSeverity } from "../lib/scanData";

function RiskChart({ findings }) {
  const count = {
    Critical: 0,
    High: 0,
    Medium: 0,
    Low: 0,
  };

  findings.forEach((f) => {
    count[normalizeSeverity(f.severity)]++;
  });

  const data = [
    { name: "Critical", value: count.Critical },
    { name: "High", value: count.High },
    { name: "Medium", value: count.Medium },
    { name: "Low", value: count.Low },
  ].filter((item) => item.value > 0);

  const COLORS = ["#fb7185", "#f87171", "#f59e0b", "#34d399"];

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-6 shadow-xl shadow-slate-950/30">
      <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
        Risk Distribution
      </h3>

      {findings.length === 0 ? (
        <p className="mt-5 text-sm text-slate-400">Run scan to see analytics.</p>
      ) : (
        <PieChart width={300} height={230}>
          <Pie
            data={data}
            dataKey="value"
            outerRadius={80}
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
