from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.core.supabase import get_service_client
from app.dependencies import get_current_user
from app.services.anomaly import AnomalyDetector

router = APIRouter(prefix="/api", tags=["analysis"])


def owned_project(project_id: str, user_id: str) -> None:
    row = get_service_client().table("projects").select("id").eq("id", project_id).eq("user_id", user_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")


def window_key(value: str | None) -> str:
    if not value:
        return "unknown"
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0).isoformat()
    except ValueError:
        return value[:16]


@router.post("/analyze")
def analyze(project_id: str, user: dict = Depends(get_current_user)):
    owned_project(project_id, user["id"])
    db = get_service_client()
    rows = db.table("logs").select("*").eq("project_id", project_id).order("timestamp").limit(5000).execute().data or []
    windows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        windows[window_key(row.get("timestamp"))].append(row)
    if len(windows) < 2:
        return {"project_id": project_id, "analyzed": len(rows), "windows": len(windows), "anomalies": 0, "message": "Need at least two time windows for Isolation Forest"}
    matrix = [AnomalyDetector.features_from_logs(items)[0] for items in windows.values()]
    detector = AnomalyDetector(contamination=min(0.2, max(1 / len(matrix), 0.01)))
    import numpy as np
    feature_matrix = np.vstack(matrix)
    detector.fit(feature_matrix)
    predictions = detector.predict(feature_matrix)
    anomalies_found = 0
    for (key, items), prediction in zip(windows.items(), predictions):
        if not prediction["is_anomaly"]:
            continue
        anomalies_found += 1
        db.table("logs").update({"anomaly_score": prediction["anomaly_score"], "is_anomaly": True}).eq("project_id", project_id).in_("id", [x["id"] for x in items if x.get("id")]).execute()
        db.table("incidents").insert({"project_id": project_id, "title": "Unusual log activity detected", "severity": "high", "description": f"Anomalous 5-minute window starting {key}; score {prediction['anomaly_score']:.4f}", "status": "open"}).execute()
    return {"project_id": project_id, "analyzed": len(rows), "windows": len(windows), "anomalies": anomalies_found}


@router.get("/anomalies")
def anomalies(project_id: str, user: dict = Depends(get_current_user)):
    owned_project(project_id, user["id"])
    rows = get_service_client().table("logs").select("*").eq("project_id", project_id).eq("is_anomaly", True).order("timestamp", desc=True).limit(500).execute().data or []
    return {"project_id": project_id, "anomalies": rows}
