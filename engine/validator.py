import pandas as pd
import pandera as pa
import pandera.errors as pa_errors


class ValidationResult:
    def __init__(self):
        self.metrics = {}
        self.violations = []


class DataValidator:
    def __init__(self, contract: dict):
        self.contract = contract

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult()

        features = self.contract.get("features", {})

        for feature_name, spec in features.items():
            series = df.get(feature_name)

            if series is None:
                result.violations.append(
                    {
                        "feature": feature_name,
                        "type": "missing_column",
                    }
                )
                continue

            # ---- Null rate ----
            null_rate = series.isna().mean()
            result.metrics[f"{feature_name}.null_rate"] = null_rate

            # ---- Type check (lightweight) ----
            expected_type = spec.get("type")
            result.metrics[f"{feature_name}.dtype"] = str(series.dtype)

            # ---- Range checks ----
            constraints = spec.get("constraints", {})
            if "min" in constraints:
                result.metrics[f"{feature_name}.min"] = series.min()
            if "max" in constraints:
                result.metrics[f"{feature_name}.max"] = series.max()

            # ---- Uniqueness ----
            if constraints.get("unique"):
                duplicate_ratio = 1 - series.is_unique
                result.metrics[f"{feature_name}.duplicate_ratio"] = duplicate_ratio

        result.metrics["row_count"] = len(df)

        return result
