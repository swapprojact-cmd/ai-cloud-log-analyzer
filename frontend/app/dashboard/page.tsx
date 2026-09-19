"use client";
import {useEffect,useState} from "react";
import {useRouter} from "next/navigation";
import {api,clearToken,Incident,Project,User} from "../../lib/api";

type List<T>={projects?:T[];incidents?:T[]};

type StatValue = string | number | null | undefined;
function stat(stats:Record<string,unknown>, keys:string[], fallback="0"): StatValue {
  for (const key of keys) if (stats[key] !== undefined && stats[key] !== null) return stats[key] as StatValue;
  return fallback;
}

export default function Dashboard(){
  const router=useRouter();
  const[projects,setProjects]=useState<Project[]>([]);const[incidents,setIncidents]=useState<Incident[]>([]);const[user,setUser]=useState<User|null>(null);const[stats,setStats]=useState<Record<string,unknown>>({});const[name,setName]=useState("");const[error,setError]=useState("");
  async function load(){try{const[u,p,i,s]=await Promise.all([api<{user:User}>("/api/auth/me"),api<List<Project>>("/api/projects"),api<List<Incident>>("/api/incidents"),api<Record<string,unknown>>("/api/dashboard/stats")]);setUser(u.user);setProjects(p.projects||[]);setIncidents(i.incidents||[]);setStats(s);}catch(e){clearToken();router.push("/login");}}
  useEffect(()=>{load()},[]);
  async function create(){if(!name.trim())return;try{await api("/api/projects",{method:"POST",body:JSON.stringify({name:name.trim(),description:""})});setName("");load();}catch(e){setError(e instanceof Error?e.message:"Could not create project")}}
  const openIncidents=incidents.filter(i=>i.status!=="resolved").length;
  const totalLogs=stat(stats,["total_logs","log_count","logs"]);
  const anomalies=stat(stats,["anomalies","anomaly_count","total_anomalies"]);
  const errors=stat(stats,["errors","error_count","total_errors"]);
  return <div className="app-shell"><nav className="nav container"><a className="brand" href="/dashboard"><span className="logo">AI</span><span>Cloud Log Analyzer</span></a><div className="navlinks"><a className="active" href="/dashboard">Overview</a><a href="/logs">Logs</a><a href="/incidents">Incidents</a><a href="/analytics">Analytics</a></div><button className="btn" onClick={()=>{clearToken();router.push("/login")}}>Logout</button></nav>
  <main className="container app-main"><div className="page-head"><div><div className="eyebrow"><span className="dot"/> System overview</div><h1>Good to see you, {user?.email?.split("@")[0]||"there"}.</h1><p>Monitor your projects, detect anomalies, and investigate incidents from one place.</p></div><a className="btn btn-primary" href="/logs">+ Analyze logs</a></div>
  <section className="metric-grid"><div className="card metric"><div className="label2">Total logs</div><div className="value">{String(totalLogs)}</div><div className="trend">Across your projects</div></div><div className="card metric"><div className="label2">Anomalies detected</div><div className="value">{String(anomalies)}</div><div className="trend">ML detection signals</div></div><div className="card metric"><div className="label2">Errors</div><div className="value">{String(errors)}</div><div className="trend">From analyzed logs</div></div><div className="card metric"><div className="label2">Open incidents</div><div className="value">{openIncidents}</div><div className="trend">Require investigation</div></div></section>
  <div className="dashboard-grid"><section className="card"><div className="section-title"><div><h2>Projects</h2><p className="muted">Organize logs by environment or service.</p></div><span className="badge">{projects.length} total</span></div><div className="create-row"><input className="input" placeholder="Create a new project" value={name} onChange={e=>setName(e.target.value)} onKeyDown={e=>e.key==='Enter'&&create()}/><button className="btn btn-primary" onClick={create}>Create</button></div>{projects.length===0?<div className="empty"><div className="empty-icon">⌁</div><strong>No projects yet</strong><span>Create your first project to start analyzing logs.</span></div>:<div className="list">{projects.map(p=><a className="list-item" href={`/logs?project=${p.id}`} key={p.id}><div><strong>{p.name}</strong><div className="muted small">{p.description||"Log monitoring project"}</div></div><span className="arrow">→</span></a>)}</div>}</section>
  <section className="card"><div className="section-title"><div><h2>Recent incidents</h2><p className="muted">Latest detected issues.</p></div><a className="text-link" href="/incidents">View all →</a></div>{incidents.length===0?<div className="empty"><div className="empty-icon">✓</div><strong>Everything looks quiet</strong><span>No incidents have been detected yet.</span></div>:<div className="list">{incidents.slice(0,6).map(i=><a className="list-item" href="/incidents" key={i.id}><div><strong>{i.title}</strong><div className="muted small">{i.description||"Anomaly detected"}</div></div><span className={`severity ${String(i.severity||"").toLowerCase()}`}>{i.severity}</span></a>)}</div>}</section></div>
  {error&&<div className="error" style={{marginTop:16}}>{error}</div>}
  </main></div>
}
