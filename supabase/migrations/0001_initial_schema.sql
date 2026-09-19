create extension if not exists pgcrypto;

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text not null unique,
  role text not null default 'user' check (role in ('user','admin')),
  created_at timestamptz not null default now()
);

create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  name text not null,
  description text,
  created_at timestamptz not null default now()
);

create table if not exists public.logs (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  timestamp timestamptz,
  service text,
  level text not null default 'INFO',
  message text not null,
  source text,
  anomaly_score double precision,
  is_anomaly boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.incidents (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  title text not null,
  severity text not null default 'medium' check (severity in ('low','medium','high','critical')),
  description text,
  ai_explanation text,
  status text not null default 'open' check (status in ('open','investigating','resolved')),
  created_at timestamptz not null default now(),
  resolved_at timestamptz
);

create table if not exists public.alerts (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid not null references public.incidents(id) on delete cascade,
  type text not null check (type in ('email','webhook')),
  message text not null,
  sent_at timestamptz,
  status text not null default 'pending'
);

create index if not exists idx_projects_user_id on public.projects(user_id);
create index if not exists idx_logs_project_timestamp on public.logs(project_id, timestamp desc);
create index if not exists idx_logs_anomaly on public.logs(project_id, is_anomaly);
create index if not exists idx_incidents_project_status on public.incidents(project_id, status);
create index if not exists idx_alerts_incident on public.alerts(incident_id);

alter table public.users enable row level security;
alter table public.projects enable row level security;
alter table public.logs enable row level security;
alter table public.incidents enable row level security;
alter table public.alerts enable row level security;

create policy "users can read own profile" on public.users for select using (auth.uid() = id);
create policy "users can update own profile" on public.users for update using (auth.uid() = id);

create policy "users manage own projects" on public.projects for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "users access project logs" on public.logs for all using (
  exists (select 1 from public.projects p where p.id = logs.project_id and p.user_id = auth.uid())
) with check (
  exists (select 1 from public.projects p where p.id = logs.project_id and p.user_id = auth.uid())
);

create policy "users access project incidents" on public.incidents for all using (
  exists (select 1 from public.projects p where p.id = incidents.project_id and p.user_id = auth.uid())
) with check (
  exists (select 1 from public.projects p where p.id = incidents.project_id and p.user_id = auth.uid())
);

create policy "users access incident alerts" on public.alerts for all using (
  exists (
    select 1 from public.incidents i
    join public.projects p on p.id = i.project_id
    where i.id = alerts.incident_id and p.user_id = auth.uid()
  )
) with check (
  exists (
    select 1 from public.incidents i
    join public.projects p on p.id = i.project_id
    where i.id = alerts.incident_id and p.user_id = auth.uid()
  )
);
