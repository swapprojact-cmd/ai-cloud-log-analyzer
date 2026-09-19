from __future__ import annotations

import os
from pathlib import Path

from supabase import Client, create_client


class StorageService:
    def __init__(self) -> None:
        self.bucket = os.getenv("SUPABASE_STORAGE_BUCKET", "raw-logs")
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.client: Client | None = create_client(url, key) if url and key else None

    def upload(self, project_id: str, filename: str, content: bytes) -> str:
        safe_name = Path(filename).name
        object_path = f"{project_id}/{safe_name}"
        if not self.client:
            return object_path
        self.client.storage.from_(self.bucket).upload(
            object_path,
            content,
            {"content-type": "text/plain", "upsert": "true"},
        )
        return object_path
