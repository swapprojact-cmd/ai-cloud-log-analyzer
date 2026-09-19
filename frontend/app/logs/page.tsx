"use client";

import { useState } from "react";

export default function LogsPage() {
  const [file, setFile] = useState<File | null>(null);
  return (
    <main className="min-h-screen px-6 py-10">
      <div className="mx-auto max-w-6xl">
        <h1 className="text-3xl font-bold text-white">Log Explorer</h1>
        <p className="mt-2 text-slate-400">Upload .log or .txt files for parsing and analysis.</p>
        <label className="mt-8 flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-900 p-12 text-center">
          <span className="font-semibold text-white">{file ? file.name : "Choose a log file"}</span>
          <span className="mt-2 text-sm text-slate-500">Maximum 10 MB · UTF-8 · .log/.txt</span>
          <input className="hidden" type="file" accept=".log,.txt,text/plain" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
        </label>
        <div className="mt-6 overflow-hidden rounded-xl border border-slate-800 bg-slate-900"><div className="border-b border-slate-800 px-5 py-4 font-semibold text-white">Parsed logs</div><div className="p-10 text-center text-sm text-slate-500">Upload a file to begin.</div></div>
      </div>
    </main>
  );
}
