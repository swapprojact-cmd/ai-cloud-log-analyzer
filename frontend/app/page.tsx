import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen px-6 py-16">
      <div className="mx-auto max-w-6xl">
        <div className="mb-16 max-w-3xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-cyan-400">AI Cloud Log Analyzer</p>
          <h1 className="text-5xl font-bold tracking-tight text-white md:text-7xl">Turn noisy logs into actionable incidents.</h1>
          <p className="mt-6 text-lg leading-8 text-slate-400">Upload application logs, detect unusual behavior with machine learning, and get evidence-based AI explanations for incidents.</p>
          <div className="mt-8 flex gap-4">
            <Link href="/dashboard" className="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950">Open dashboard</Link>
            <Link href="/logs" className="rounded-lg border border-slate-700 px-5 py-3 font-semibold text-white">Explore logs</Link>
          </div>
        </div>
        <div className="grid gap-5 md:grid-cols-3">
          {["Log ingestion", "ML anomaly detection", "AI incident analysis"].map((item, index) => (
            <div key={item} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
              <div className="mb-4 text-2xl">0{index + 1}</div>
              <h2 className="text-xl font-semibold text-white">{item}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-400">A focused layer of the end-to-end monitoring pipeline.</p>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
