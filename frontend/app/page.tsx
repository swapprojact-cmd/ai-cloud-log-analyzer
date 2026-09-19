import Link from "next/link";

export default function Home() {
  return (
    <main>
      <nav className="container nav">
        <div className="brand"><span className="logo">AI</span> Cloud Log Analyzer</div>
        <div className="navlinks"><Link href="/login">Sign in</Link><Link href="/register">Get started</Link></div>
      </nav>
      <section className="container hero">
        <span className="eyebrow"><span className="dot" /> Intelligent log observability</span>
        <h1>Turn noisy logs into <span className="gradient">clear incidents.</span></h1>
        <p>Upload application logs, detect unusual behavior with machine learning, and get evidence-based AI explanations in seconds.</p>
        <div className="actions"><Link className="btn btn-primary" href="/register">Start analyzing →</Link><Link className="btn" href="/login">Sign in</Link></div>
      </section>
      <section className="container features">
        <article className="card"><div className="icon">01</div><h3>Collect & explore</h3><p>Upload .log and .txt files, parse structured events, then search and filter your history.</p></article>
        <article className="card"><div className="icon">02</div><h3>Detect anomalies</h3><p>Surface unusual error, warning, request and response-time patterns with ML.</p></article>
        <article className="card"><div className="icon">03</div><h3>Explain incidents</h3><p>Give your team concise evidence-backed summaries and practical investigation steps.</p></article>
      </section>
    </main>
  );
}
