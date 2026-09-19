const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function getToken() { return typeof window === "undefined" ? null : localStorage.getItem("acl_access_token"); }
export function setToken(token: string) { localStorage.setItem("acl_access_token", token); }
export function clearToken() { localStorage.removeItem("acl_access_token"); }

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body && !(options.body instanceof FormData)) headers.set("Content-Type", "application/json");
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const text = await response.text();
  let data: unknown = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = { detail: text }; }
  if (!response.ok) throw new Error(typeof data === "object" && data && "detail" in data ? String((data as {detail: unknown}).detail) : "Request failed");
  return data as T;
}

export type Project = { id: string; name: string; description?: string | null; created_at: string };
export type LogRecord = { id: string; timestamp?: string | null; service?: string | null; level: string; message: string; source?: string | null; anomaly_score?: number | null; is_anomaly: boolean };
export type Incident = { id: string; project_id: string; title: string; severity: string; description?: string | null; ai_explanation?: string | null; status: string; created_at: string; resolved_at?: string | null };
export type User = { id: string; email?: string; name?: string; role?: string };
