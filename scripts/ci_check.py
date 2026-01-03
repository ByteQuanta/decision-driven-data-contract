import sys
import yaml

from engine.loader import DataLoader
from engine.validator import DataValidator
from engine.risk import RiskEngine


def main():
    with open("contracts/user_features.yaml") as f:
        contract = yaml.safe_load(f)

    loader = DataLoader("data/incoming")
    df = loader.load_latest()

    validator = DataValidator(contract)
    result = validator.validate(df)

    risk = RiskEngine(contract).compute(result.metrics)

    if risk.score >= 0.4:
        print("❌ DATA CONTRACT VIOLATION")
        print(f"Risk score: {risk.score}")
        for reason in risk.reasons:
            print(f"- {reason}")
        sys.exit(1)

    print("✅ Data contract check passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
