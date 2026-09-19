from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest


FEATURE_NAMES = (
    "error_count",
    "warning_count",
    "request_count",
    "response_time",
    "unique_error_types",
    "log_frequency",
)


class AnomalyDetector:
    """Baseline Isolation Forest detector for aggregated log windows."""

    def __init__(self, contamination: float = 0.05, random_state: int = 42) -> None:
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=200,
        )
        self._fitted = False

    @staticmethod
    def features_from_logs(logs: list[dict[str, Any]]) -> np.ndarray:
        errors = [x for x in logs if str(x.get("level", "")).upper() in {"ERROR", "CRITICAL", "FATAL"}]
        warnings = [x for x in logs if str(x.get("level", "")).upper() == "WARN"]
        messages = {str(x.get("message", "")) for x in errors}
        response_times = [float(x["response_time"]) for x in logs if x.get("response_time") is not None]
        response_time = float(np.mean(response_times)) if response_times else 0.0
        return np.array([[len(errors), len(warnings), len(logs), response_time, len(messages), len(logs)]], dtype=float)

    def fit(self, feature_matrix: np.ndarray) -> None:
        if len(feature_matrix) < 2:
            raise ValueError("At least two feature rows are required to fit the anomaly detector.")
        self.model.fit(feature_matrix)
        self._fitted = True

    def predict(self, feature_matrix: np.ndarray) -> list[dict[str, float | bool]]:
        if not self._fitted:
            raise RuntimeError("Anomaly detector must be fitted before prediction.")
        labels = self.model.predict(feature_matrix)
        scores = -self.model.decision_function(feature_matrix)
        return [{"is_anomaly": bool(label == -1), "anomaly_score": float(score)} for label, score in zip(labels, scores)]
