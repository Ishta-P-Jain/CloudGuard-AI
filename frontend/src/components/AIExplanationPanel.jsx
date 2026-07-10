function Section({ title, children }) {
  return (
    <section className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
      <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-400">{title}</h3>
      <div className="mt-3 text-sm leading-6 text-slate-200">{children}</div>
    </section>
  );
}

function Checklist({ steps }) {
  if (!steps || steps.length === 0) {
    return <p className="text-slate-400">No remediation steps were returned yet.</p>;
  }

  return (
    <ol className="space-y-3">
      {steps.map((step, index) => (
        <li className="flex gap-3" key={`${step}-${index}`}>
          <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-cyan-400/40 bg-cyan-400/10 text-xs font-bold text-cyan-200">
            {index + 1}
          </span>
          <span>{step}</span>
        </li>
      ))}
    </ol>
  );
}

export default function AIExplanationPanel({ explanation, error, finding, loading, onClose }) {
  return (
    <aside className="rounded-lg border border-slate-800 bg-slate-900 shadow-xl shadow-slate-950/30">
      <div className="flex items-start justify-between gap-4 border-b border-slate-800 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-cyan-200">AI Explain & Fix</p>
          <h2 className="mt-1 text-lg font-bold text-white">
            {finding ? finding.title : "Select a finding"}
          </h2>
        </div>
        {finding && (
          <button
            className="rounded-lg border border-slate-700 px-3 py-1.5 text-sm text-slate-300 transition hover:border-slate-500 hover:text-white"
            onClick={onClose}
            type="button"
          >
            Close
          </button>
        )}
      </div>

      <div className="space-y-4 p-5">
        {!finding ? (
          <div className="rounded-lg border border-dashed border-slate-700 p-6 text-center">
            <p className="font-medium text-white">No finding selected</p>
            <p className="mt-2 text-sm text-slate-400">
              Click Explain/Fix on a finding to view the AI explanation and remediation checklist.
            </p>
          </div>
        ) : loading ? (
          <div className="space-y-4">
            <div className="h-3 w-3/4 animate-pulse rounded bg-slate-700" />
            <div className="h-24 animate-pulse rounded-lg bg-slate-800" />
            <div className="h-24 animate-pulse rounded-lg bg-slate-800" />
          </div>
        ) : error ? (
          <div className="rounded-lg border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-100">
            {error}
          </div>
        ) : explanation ? (
          <>
            <Section title="Explanation">
              <p>{explanation.explanation}</p>
            </Section>

            <Section title="Why It Matters">
              <p>{explanation.danger}</p>
            </Section>

            <Section title="Real World Impact">
              <p>{explanation.realWorldImpact}</p>
            </Section>

            <Section title="Remediation Checklist">
              <Checklist steps={explanation.remediationSteps} />
            </Section>

            <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm text-emerald-100">
              Estimated effort: <span className="font-semibold">{explanation.estimatedEffort}</span>
            </div>
          </>
        ) : (
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4 text-sm text-slate-300">
            Ready to request an AI explanation for this finding.
          </div>
        )}
      </div>
    </aside>
  );
}

