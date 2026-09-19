from __future__ import annotations

from datetime import datetime
import re
from typing import Any

LEVELS = {"DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "FATAL"}


class LogParser:
    """Parse common timestamp/level/service/message log lines.

    The parser is intentionally conservative: unmatched lines are retained
    instead of being discarded so evidence is not silently lost.
    """

    _pattern = re.compile(
        r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[T ][\d:.+\-Z]+)?\s*"
        r"(?:\[(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\]|(?P<level2>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL))?\s*"
        r"(?:\[(?P<service>[^\]]+)\]|(?P<service2>[\w.-]+))?\s*[-:]?\s*"
        r"(?P<message>.*)$",
        re.IGNORECASE,
    )

    def parse_line(self, line: str, source: str = "upload") -> dict[str, Any]:
        raw = line.rstrip("\n\r")
        match = self._pattern.match(raw)
        if not match:
            return {"timestamp": None, "service": None, "level": "INFO", "message": raw, "source": source}

        data = match.groupdict()
        timestamp = self._parse_timestamp(data.get("timestamp"))
        level = (data.get("level") or data.get("level2") or "INFO").upper()
        if level == "WARNING":
            level = "WARN"
        service = data.get("service") or data.get("service2")
        message = (data.get("message") or "").strip()
        return {"timestamp": timestamp, "service": service, "level": level, "message": message, "source": source}

    @staticmethod
    def _parse_timestamp(value: str | None) -> datetime | None:
        if not value:
            return None
        normalized = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            return None

    def parse_text(self, text: str, source: str = "upload") -> list[dict[str, Any]]:
        return [self.parse_line(line, source) for line in text.splitlines() if line.strip()]
