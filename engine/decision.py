class Decision:
    def __init__(self, name: str, severity: str, reason: str):
        self.name = name
        self.severity = severity
        self.reason = reason

    def __repr__(self):
        return (
            f"Decision(name={self.name}, "
            f"severity={self.severity}, "
            f"reason={self.reason})"
        )


class DecisionEngine:
    def __init__(self, contract: dict):
        self.contract = contract

    def decide(self, risk_score) -> Decision:
        score = risk_score.score

        if score >= 0.7:
            return Decision(
                name="BLOCK_AND_ROLLBACK",
                severity="CRITICAL",
                reason="High risk of silent data corruption",
            )

        if score >= 0.4:
            return Decision(
                name="ALLOW_WITH_ALERT",
                severity="WARN",
                reason="Moderate data quality risk detected",
            )

        return Decision(
            name="ALLOW",
            severity="INFO",
            reason="Data within acceptable risk thresholds",
        )
