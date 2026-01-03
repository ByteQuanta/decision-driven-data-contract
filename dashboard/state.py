import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta


class SystemState:
    def __init__(
        self,
        decision_log_path="decisions/decision_log.jsonl",
        lookback_hours=24,
    ):
        self.decision_log_path = Path(decision_log_path)
        self.lookback_hours = lookback_hours

        self.decisions = []
        self._load()

    def _load(self):
        if not self.decision_log_path.exists():
            return

        cutoff = datetime.utcnow() - timedelta(hours=self.lookback_hours)

        with open(self.decision_log_path, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                ts = datetime.fromisoformat(record["timestamp"])

                if ts >= cutoff:
                    self.decisions.append(record)

    # ---------- High-level summaries ----------

    def total_events(self) -> int:
        return len(self.decisions)

    def decision_counts(self) -> dict:
        return Counter(d["decision"] for d in self.decisions)

    def severity_counts(self) -> dict:
        return Counter(d["severity"] for d in self.decisions)

    def latest_decision(self) -> dict | None:
        if not self.decisions:
            return None
        return max(self.decisions, key=lambda d: d["timestamp"])

    # ---------- Risk & feature insights ----------

    def risk_trend(self) -> list[float]:
        """
        Returns risk scores ordered by time.
        (Risk score is inferred from decision severity.)
        """
        severity_to_risk = {
            "INFO": 0.0,
            "WARN": 0.5,
            "CRITICAL": 1.0,
        }

        return [
            severity_to_risk.get(d["severity"], 0.0)
            for d in sorted(self.decisions, key=lambda d: d["timestamp"])
        ]

    def frequent_reasons(self, top_k=3) -> dict:
        reasons = Counter(d["reason"] for d in self.decisions)
        return dict(reasons.most_common(top_k))

    # ---------- Health signal ----------

    def system_health(self) -> str:
        """
        Coarse system health indicator for executives.
        """
        counts = self.severity_counts()

        if counts.get("CRITICAL", 0) > 0:
            return "RED"

        if counts.get("WARN", 0) > 0:
            return "YELLOW"

        return "GREEN"
