"use client";
import {FormEvent,useState} from "react";
import {useRouter} from "next/navigation";
import {api,setToken} from "../../lib/api";
import Link from "next/link";

export default function Login(){
 const router=useRouter(); const[email,setEmail]=useState(""); const[password,setPassword]=useState(""); const[error,setError]=useState(""); const[busy,setBusy]=useState(false);
 async function submit(e:FormEvent){e.preventDefault();setBusy(true);setError("");try{const r=await api<{access_token:string}>("/api/auth/login",{method:"POST",body:JSON.stringify({email,password})});setToken(r.access_token);router.push("/dashboard");}catch(err){setError(err instanceof Error?err.message:"Login failed");}finally{setBusy(false);}}
 return <main className="auth-wrap"><div className="auth-card"><div className="brand" style={{justifyContent:"center",marginBottom:22}}><span className="logo">AI</span> Cloud Log Analyzer</div><div className="card"><h1>Welcome back</h1><p className="sub">Sign in to investigate your cloud logs and incidents.</p><form className="form" onSubmit={submit}><label className="label">Email<input className="input" required type="email" placeholder="you@company.com" value={email} onChange={e=>setEmail(e.target.value)}/></label><label className="label">Password<input className="input" required type="password" placeholder="Your password" value={password} onChange={e=>setPassword(e.target.value)}/></label>{error&&<div className="error">{error}</div>}<button className="btn btn-primary" disabled={busy}>{busy?"Signing in…":"Sign in"}</button></form><div className="auth-footer">Don't have an account? <Link href="/register">Create one</Link></div></div></div></main>;
}
