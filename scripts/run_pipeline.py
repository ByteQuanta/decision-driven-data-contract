import yaml

from engine.loader import DataLoader
from engine.validator import DataValidator
from engine.risk import RiskEngine
from engine.decision import DecisionEngine
from engine.actions import ActionExecutor


def run():
    # Load contract
    with open("contracts/user_features.yaml") as f:
        contract = yaml.safe_load(f)

    # Load latest data
    loader = DataLoader("data/incoming")
    df = loader.load_latest()

    # Validate & compute risk
    validator = DataValidator(contract)
    metrics = validator.validate(df).metrics

    risk_engine = RiskEngine(contract)
    risk = risk_engine.compute(metrics)

    # Decide
    decision_engine = DecisionEngine(contract)
    decision = decision_engine.decide(risk)

    # Act
    executor = ActionExecutor()
    log = executor.execute(decision, df)

    # Console output (ops-friendly)
    print("=== DATA CONTRACT PIPELINE RESULT ===")
    print(f"Decision : {decision.name}")
    print(f"Severity : {decision.severity}")
    print(f"Reason   : {decision.reason}")
    print(f"Risk     : {risk.score}")
    print("=====================================")

    return log


if __name__ == "__main__":
    run()
