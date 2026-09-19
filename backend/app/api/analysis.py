from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.supabase import get_service_client
from app.dependencies import get_current_user
from app.services.anomaly import AnomalyDetector

router = APIRouter(prefix="/api", tags=["analysis"])


def owned_project(project_id: str, user_id: str) -> None:
    row = get_service_client().table("projects").select("id").eq("id", project_id).eq("user_id", user_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/analyze")
def analyze(project_id: str, user: dict = Depends(get_current_user)):
    owned_project(project_id, user["id"])
    db = get_service_client()
    rows = db.table("logs").select("*").eq("project_id", project_id).order("timestamp").limit(5000).execute().data or []
    if len(rows) < 2:
        return {"project_id": project_id, "analyzed": len(rows), "anomalies": 0, "message": "Not enough logs for anomaly detection"}
    detector = AnomalyDetector()
    features = detector.features_from_logs(rows)
    # The current detector is intentionally conservative for the MVP; one aggregate feature row is scored as a project-level signal.
    score = float(detector.predict(features)[0]) if hasattr(detector, "predict") else 0.0
    is_anomaly = score < 0
    if is_anomaly:
        db.table("incidents").insert({"project_id": project_id, "title": "Unusual log activity detected", "severity": "high", "description": f"Aggregate anomaly score: {score:.4f}", "status": "open"}).execute()
    return {"project_id": project_id, "analyzed": len(rows), "anomalies": 1 if is_anomaly else 0, "anomaly_score": score}


@router.get("/anomalies")
def anomalies(project_id: str, user: dict = Depends(get_current_user)):
    owned_project(project_id, user["id"])
    rows = get_service_client().table("logs").select("*").eq("project_id", project_id).eq("is_anomaly", True).order("timestamp", desc=True).limit(500).execute().data or []
    return {"project_id": project_id, "anomalies": rows}
