const stats = [
  ["Total logs", "0"],
  ["Errors", "0"],
  ["Warnings", "0"],
  ["Anomalies", "0"],
  ["Open incidents", "0"],
];

export default function DashboardPage() {
  return (
    <main className="min-h-screen px-6 py-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-10"><p className="text-sm text-cyan-400">MONITORING</p><h1 className="mt-2 text-3xl font-bold text-white">Dashboard</h1><p className="mt-2 text-slate-400">Operational overview of your project logs and incidents.</p></header>
        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {stats.map(([label, value]) => <div key={label} className="rounded-xl border border-slate-800 bg-slate-900 p-5"><p className="text-sm text-slate-400">{label}</p><p className="mt-3 text-3xl font-bold text-white">{value}</p></div>)}
        </section>
        <section className="mt-6 grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6"><h2 className="text-lg font-semibold text-white">Error trends</h2><div className="mt-8 flex h-48 items-center justify-center rounded-lg border border-dashed border-slate-700 text-sm text-slate-500">No trend data yet</div></div>
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6"><h2 className="text-lg font-semibold text-white">Recent incidents</h2><div className="mt-8 flex h-48 items-center justify-center rounded-lg border border-dashed border-slate-700 text-sm text-slate-500">No incidents yet</div></div>
        </section>
      </div>
    </main>
  );
}
