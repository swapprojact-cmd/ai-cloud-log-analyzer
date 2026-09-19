from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.supabase import get_service_client
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def project_ids(user_id: str) -> list[str]:
    rows = get_service_client().table("projects").select("id").eq("user_id", user_id).execute().data or []
    return [row["id"] for row in rows]


@router.get("/stats")
def stats(user: dict = Depends(get_current_user)):
    ids = project_ids(user["id"])
    if not ids:
        return {"total_logs": 0, "errors": 0, "warnings": 0, "anomalies": 0, "open_incidents": 0}
    db = get_service_client()
    logs = db.table("logs").select("level,is_anomaly").in_("project_id", ids).execute().data or []
    incidents = db.table("incidents").select("status").in_("project_id", ids).execute().data or []
    return {
        "total_logs": len(logs),
        "errors": sum(1 for row in logs if str(row.get("level", "")).lower() == "error"),
        "warnings": sum(1 for row in logs if str(row.get("level", "")).lower() in {"warning", "warn"}),
        "anomalies": sum(1 for row in logs if row.get("is_anomaly") is True),
        "open_incidents": sum(1 for row in incidents if row.get("status") != "resolved"),
    }


@router.get("/trends")
def trends(user: dict = Depends(get_current_user)):
    ids = project_ids(user["id"])
    if not ids:
        return {"trends": []}
    rows = get_service_client().table("logs").select("timestamp,level").in_("project_id", ids).order("timestamp", desc=False).limit(5000).execute().data or []
    buckets: dict[str, dict] = {}
    for row in rows:
        day = str(row.get("timestamp", ""))[:10]
        if not day:
            continue
        bucket = buckets.setdefault(day, {"date": day, "logs": 0, "errors": 0, "warnings": 0})
        bucket["logs"] += 1
        level = str(row.get("level", "")).lower()
        if level == "error": bucket["errors"] += 1
        if level in {"warning", "warn"}: bucket["warnings"] += 1
    return {"trends": list(buckets.values())[-30:]}
