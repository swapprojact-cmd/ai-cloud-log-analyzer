from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, dashboard, incidents, logs, projects
from app.core.config import settings

app = FastAPI(
    title="AI Cloud Log Analyzer API",
    version="0.2.0",
    description="API for log ingestion, anomaly detection, incidents, and AI-assisted analysis.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(logs.router)
app.include_router(incidents.router)
app.include_router(dashboard.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
