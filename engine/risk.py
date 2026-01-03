class RiskScore:
    def __init__(self, score: float, reasons: list):
        self.score = round(score, 2)
        self.reasons = reasons

    def __repr__(self):
        return f"RiskScore(score={self.score}, reasons={self.reasons})"


class RiskEngine:
    def __init__(self, contract: dict):
        self.contract = contract

    def compute(self, metrics: dict) -> RiskScore:
        score = 0.0
        reasons = []

        features = self.contract.get("features", {})

        for feature_name, spec in features.items():
            criticality = spec.get("criticality", "tier_2")

            # weight by criticality
            if criticality == "tier_1":
                weight = 1.0
            else:
                weight = 0.5

            # ---- Null rate risk ----
            null_key = f"{feature_name}.null_rate"
            if null_key in metrics:
                null_rate = float(metrics[null_key])
                score += null_rate * weight

                if null_rate > 0:
                    reasons.append(
                        f"{feature_name}: null_rate={round(null_rate, 2)}"
                    )

        return RiskScore(score=score, reasons=reasons)
