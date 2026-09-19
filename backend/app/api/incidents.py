from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.supabase import get_service_client
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


class IncidentUpdate(BaseModel):
    status: str | None = Field(default=None, pattern="^(open|investigating|resolved)$")
    severity: str | None = Field(default=None, pattern="^(low|medium|high|critical)$")


def owned_incident(incident_id: str, user_id: str) -> dict:
    result = get_service_client().table("incidents").select("*").eq("id", incident_id).maybe_single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Incident not found")
    project = get_service_client().table("projects").select("id").eq("id", result.data["project_id"]).eq("user_id", user_id).maybe_single().execute()
    if not project.data:
        raise HTTPException(status_code=404, detail="Incident not found")
    return result.data


@router.get("")
def list_incidents(project_id: str | None = None, user: dict = Depends(get_current_user)):
    projects = get_service_client().table("projects").select("id").eq("user_id", user["id"]).execute().data or []
    ids = [p["id"] for p in projects]
    if not ids:
        return {"incidents": []}
    query = get_service_client().table("incidents").select("*").in_("project_id", ids).order("created_at", desc=True)
    if project_id:
        if project_id not in ids:
            raise HTTPException(status_code=404, detail="Project not found")
        query = query.eq("project_id", project_id)
    return {"incidents": query.execute().data or []}


@router.get("/{incident_id}")
def get_incident(incident_id: str, user: dict = Depends(get_current_user)):
    return owned_incident(incident_id, user["id"])


@router.patch("/{incident_id}")
def update_incident(incident_id: str, payload: IncidentUpdate, user: dict = Depends(get_current_user)):
    owned_incident(incident_id, user["id"])
    changes = {k: v for k, v in payload.model_dump().items() if v is not None}
    result = get_service_client().table("incidents").update(changes).eq("id", incident_id).execute()
    return result.data[0] if result.data else {"id": incident_id, **changes}
