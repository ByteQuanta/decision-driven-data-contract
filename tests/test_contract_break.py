import yaml
import pandas as pd
from engine.validator import DataValidator
from engine.risk import RiskEngine
from engine.decision import DecisionEngine


def test_contract_break_on_high_null_rate():
    """
    GIVEN intentionally broken data
    WHEN data contract is evaluated
    THEN ingestion must NOT be allowed
    """

    # --- Load contract ---
    with open("contracts/user_features.yaml") as f:
        contract = yaml.safe_load(f)

    # --- Create intentionally bad data ---
    df = pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4],
            "user_age": [None, None, None, None],  # 100% null
            "country_code": ["TR", "DE", "US", "FR"],
            "signup_days_ago": [10, 20, 30, 40],
        }
    )

    # --- Validate ---
    validator = DataValidator(contract)
    metrics = validator.validate(df).metrics

    # --- Compute risk ---
    risk = RiskEngine(contract).compute(metrics)

    # --- Decide ---
    decision = DecisionEngine(contract).decide(risk)

    # --- Assert guardrail ---
    assert decision.name != "ALLOW", "Broken data should never be allowed"
