"use client";
import {FormEvent,useState} from "react";
import {useRouter} from "next/navigation";
import {api,setToken,AuthResponse} from "../../lib/api";
import Link from "next/link";

export default function Register(){
 const router=useRouter(); const[email,setEmail]=useState(""); const[password,setPassword]=useState(""); const[error,setError]=useState(""); const[busy,setBusy]=useState(false);
 async function submit(e:FormEvent){e.preventDefault();setBusy(true);setError("");try{const r=await api<AuthResponse>("/api/auth/register",{method:"POST",body:JSON.stringify({email,password})});if(r.access_token){setToken(r.access_token);router.push("/dashboard");}else router.push("/login?registered=1");}catch(err){setError(err instanceof Error?err.message:"Registration failed");}finally{setBusy(false);}}
 return <main className="auth-wrap"><div className="auth-card"><div className="brand" style={{justifyContent:"center",marginBottom:22}}><span className="logo">AI</span> Cloud Log Analyzer</div><div className="card"><h1>Create your account</h1><p className="sub">Start turning raw logs into actionable incidents.</p><form className="form" onSubmit={submit}><label className="label">Email<input className="input" required type="email" placeholder="you@company.com" value={email} onChange={e=>setEmail(e.target.value)}/></label><label className="label">Password<input className="input" required minLength={8} type="password" placeholder="At least 8 characters" value={password} onChange={e=>setPassword(e.target.value)}/></label>{error&&<div className="error">{error}</div>}<button className="btn btn-primary" disabled={busy}>{busy?"Creating account…":"Create account"}</button></form><div className="auth-footer">Already have an account? <Link href="/login">Sign in</Link></div></div></div></main>;
}
