alter table public.users alter column name drop not null;
alter table public.users alter column name set default '';

insert into storage.buckets (id, name, public)
values ('raw-logs', 'raw-logs', false)
on conflict (id) do nothing;

create policy "authenticated users upload own raw logs" on storage.objects
for insert to authenticated
with check (bucket_id = 'raw-logs' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "authenticated users read own raw logs" on storage.objects
for select to authenticated
using (bucket_id = 'raw-logs' and (storage.foldername(name))[1] = auth.uid()::text);
