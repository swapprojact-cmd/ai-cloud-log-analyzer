import Link from "next/link";

export default function Home() {
  return <main style={{maxWidth:900,margin:"80px auto",padding:24,fontFamily:"sans-serif"}}><h1>AI Cloud Log Analyzer</h1><p>Upload, analyze and investigate application logs with ML anomaly detection and AI explanations.</p><div style={{display:"flex",gap:12}}><Link href="/login">Login</Link><Link href="/register">Create account</Link></div></main>;
}
