from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.get("")
def list_incidents(project_id: str) -> dict:
    return {"project_id": project_id, "incidents": []}


@router.get("/{incident_id}")
def get_incident(incident_id: str) -> dict:
    return {"id": incident_id, "status": "open"}


@router.patch("/{incident_id}")
def update_incident(incident_id: str, payload: dict) -> dict:
    return {"id": incident_id, **payload}
