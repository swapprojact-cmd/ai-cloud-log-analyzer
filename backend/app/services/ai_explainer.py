from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


class AIExplainer:
    """Generate incident explanations from supplied evidence only."""

    def __init__(self, client: OpenAI | None = None, model: str | None = None) -> None:
        self.client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")

    def explain(self, incident: dict[str, Any], evidence: list[dict[str, Any]]) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "You are an incident-analysis assistant. Use only the supplied evidence. "
                "Do not claim a root cause unless the evidence establishes it. "
                "Return a concise explanation, evidence summary, and investigation checklist."
            ),
            input=[
                {"role": "user", "content": [{"type": "input_text", "text": f"Incident: {incident}"}]},
                {"role": "user", "content": [{"type": "input_text", "text": f"Evidence: {evidence}"}]},
            ],
        )
        return response.output_text
