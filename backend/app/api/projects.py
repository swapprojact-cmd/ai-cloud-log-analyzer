from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.supabase import get_service_client
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


@router.get("")
def list_projects(user: dict = Depends(get_current_user)):
    result = get_service_client().table("projects").select("*").eq("user_id", user["id"]).order("created_at", desc=True).execute()
    return {"projects": result.data or []}


@router.post("")
def create_project(payload: ProjectCreate, user: dict = Depends(get_current_user)):
    result = get_service_client().table("projects").insert({"user_id": user["id"], **payload.model_dump()}).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Project creation failed")
    return result.data[0]


@router.delete("/{project_id}")
def delete_project(project_id: str, user: dict = Depends(get_current_user)):
    result = get_service_client().table("projects").delete().eq("id", project_id).eq("user_id", user["id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"deleted": True, "id": project_id}
