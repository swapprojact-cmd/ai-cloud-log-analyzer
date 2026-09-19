from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.parser import LogParser

router = APIRouter(prefix="/api/logs", tags=["logs"])
parser = LogParser()


@router.post("/upload")
async def upload_logs(project_id: str, file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.lower().endswith((".log", ".txt")):
        raise HTTPException(status_code=400, detail="Only .log and .txt files are supported")
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB upload limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded") from exc
    records = parser.parse_text(text, source=file.filename)
    return {"project_id": project_id, "filename": file.filename, "count": len(records), "logs": records}


@router.post("")
def create_log(project_id: str, payload: dict) -> dict:
    payload["project_id"] = project_id
    return payload


@router.get("")
def list_logs(project_id: str, limit: int = 100) -> dict:
    return {"project_id": project_id, "limit": min(limit, 500), "logs": []}
