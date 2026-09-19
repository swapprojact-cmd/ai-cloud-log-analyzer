from fastapi import APIRouter

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
def dashboard_stats(project_id: str) -> dict:
    return {
        "project_id": project_id,
        "total_logs": 0,
        "errors": 0,
        "warnings": 0,
        "anomalies": 0,
        "open_incidents": 0,
    }


@router.get("/trends")
def dashboard_trends(project_id: str) -> dict:
    return {"project_id": project_id, "trends": []}
