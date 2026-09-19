"use client";
import {FormEvent, useState} from "react";
import {useRouter} from "next/navigation";
import {api, setToken} from "../../lib/api";

export default function Login() {
  const router=useRouter(); const [email,setEmail]=useState(""); const [password,setPassword]=useState(""); const [error,setError]=useState(""); const [busy,setBusy]=useState(false);
  async function submit(e:FormEvent){e.preventDefault();setBusy(true);setError("");try{const r=await api<{access_token:string}>("/api/auth/login",{method:"POST",body:JSON.stringify({email,password})});setToken(r.access_token);router.push("/dashboard");}catch(err){setError(err instanceof Error?err.message:"Login failed");}finally{setBusy(false);}}
  return <main style={{maxWidth:420,margin:"80px auto",padding:24,fontFamily:"sans-serif"}}><h1>Login</h1><form onSubmit={submit} style={{display:"grid",gap:12}}><input required type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/><input required type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)}/><button disabled={busy}>{busy?"Signing in…":"Sign in"}</button>{error&&<p>{error}</p>}</form></main>;
}
