from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.supabase import get_service_client
from app.dependencies import get_current_user
from app.services.parser import LogParser
from app.services.storage import StorageService

router = APIRouter(prefix="/api/logs", tags=["logs"])
parser = LogParser()
storage = StorageService()


def owned_project(project_id: str, user_id: str) -> dict:
    result = get_service_client().table("projects").select("id").eq("id", project_id).eq("user_id", user_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return result.data


@router.post("/upload")
async def upload_logs(project_id: str, file: UploadFile = File(...), user: dict = Depends(get_current_user)) -> dict:
    owned_project(project_id, user["id"])
    if not file.filename or not file.filename.lower().endswith((".log", ".txt")):
        raise HTTPException(status_code=400, detail="Only .log and .txt files are supported")
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB upload limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded") from exc
    object_path = storage.upload(project_id, file.filename, raw)
    records = parser.parse_text(text, source=file.filename)
    rows = [{"project_id": project_id, **record} for record in records]
    if rows:
        get_service_client().table("logs").insert(rows).execute()
    return {"project_id": project_id, "filename": file.filename, "storage_path": object_path, "count": len(rows)}


@router.post("")
def create_log(project_id: str, payload: dict, user: dict = Depends(get_current_user)):
    owned_project(project_id, user["id"])
    result = get_service_client().table("logs").insert({"project_id": project_id, **payload}).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Log creation failed")
    return result.data[0]


@router.get("")
def list_logs(project_id: str, limit: int = 100, user: dict = Depends(get_current_user)):
    owned_project(project_id, user["id"])
    result = get_service_client().table("logs").select("*").eq("project_id", project_id).order("timestamp", desc=True).limit(min(limit, 500)).execute()
    return {"project_id": project_id, "logs": result.data or []}


@router.delete("/{log_id}")
def delete_log(log_id: str, user: dict = Depends(get_current_user)):
    row = get_service_client().table("logs").select("id,project_id").eq("id", log_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Log not found")
    owned_project(row["project_id"], user["id"])
    get_service_client().table("logs").delete().eq("id", log_id).execute()
    return {"deleted": True, "id": log_id}
