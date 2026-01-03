# Decision-Driven Data Contract & Monitoring System

A production-grade data contract system that **measures data quality risk**, **makes automated ingestion decisions**, and **enforces feature-level SLAs** — without notebooks, dashboards no one checks, or manual intervention.

This project is not about validating data.

It is about **deciding what happens when data quality degrades**.

---

## 🚨 The Real Problem

Most data quality systems stop at:
- schema checks
- null counts
- dashboards

But production systems don’t fail because metrics exist.  
They fail because **no decision is enforced when data breaks**.

> What should the system do when incoming data is *technically valid*  
> but *operationally dangerous*?

This project answers that question end-to-end.

---

## 🧠 Design Philosophy

**Checks ≠ Decisions**  
**Metrics ≠ Actions**

This system explicitly separates:

1. **Measurement** – What is the data quality?
2. **Risk Assessment** – How risky is this for downstream systems?
3. **Decision** – Should we allow, warn, or block ingestion?
4. **Action** – What actually happens in the pipeline?
5. **Auditability** – Why did this decision happen?

This separation mirrors how real ML and data platforms operate at scale.

---

## 🏗️ High-Level Architecture

```
Incoming CSVs
│
▼
Data Contract (YAML)
│
▼
Validator ──► Quality Metrics
│
▼
Risk Engine ──► Risk Score
│
▼
Decision Engine ──► ALLOW / WARN / BLOCK
│
▼
Actions + Audit Log

The system does not ask humans to interpret dashboards.  
It **decides and acts automatically**.

---

## 📦 Project Structure

```
data_contract/
├── engine/ # Core decision logic
│ ├── loader.py # Load latest incoming data
│ ├── validator.py # Compute quality metrics
│ ├── risk.py # Metrics → risk
│ ├── decision.py # Risk → decision
│ └── actions.py # Enforced outcomes
│
├── dashboard/
│ ├── state.py # Derive system state from logs
│ └── app.py # CLI operational dashboard
│
├── contracts/ # Data contracts (YAML)
├── scripts/ # Entry points & CI guardrails
├── tests/ # Failure simulation tests
│
├── contract_check.yml # Policy as code
├── pyproject.toml
└── environment.yml

---

## 📜 Data Contract Example

```yaml
dataset:
  name: user_features

features:
  user_id:
    dtype: int
    allow_null: false
    max_null_rate: 0.0

  user_age:
    dtype: float
    allow_null: true
    max_null_rate: 0.3

  country_code:
    dtype: str
    allow_null: false

  signup_days_ago:
    dtype: int
    min: 0
    max: 3650
```

Contracts define expectations, not behavior.

---

## ⚖️ Risk-Based Decisions

Instead of binary pass/fail checks, the system computes operational risk.

| Risk Score | Decision           | Meaning                        |
| ---------- | ------------------ | ------------------------------ |
| `< 0.25`   | ALLOW              | Safe to ingest                 |
| `0.25–0.4` | ALLOW_WITH_ALERT   | Monitor closely                |
| `≥ 0.4`    | BLOCK_AND_ROLLBACK | Prevent silent data corruption |

---

## 🧪 Failure Simulation (Not Happy Paths)

The system is explicitly tested against bad data scenarios.

```bash
pytest tests/test_contract_break.py

```

If risky data passes, tests fail.

This ensures enforcement, not observability theater.

---

## 🛡️ Policy as Code

Organizational guardrails live outside Python:

```yaml
risk:
  block_threshold: 0.4

ci:
  fail_on:
    - block

```

Changing enforcement rules does not require code changes.

---

## 📊 Operational Dashboard (CLI)
```bash
python -m dashboard.app

```

Shows:

- current system health

- recent decisions

- most frequent issues

The goal is not visualization.
The goal is operational clarity.

---

# 🚀 Running the Pipeline
```bash
pip install -e .
python -m scripts.run_pipeline

```

CI enforcement:
```bash
python -m scripts.ci_check

```

---

## 💡 Why This Matters

- No notebooks

- No manual inspection

- No “we’ll check it later”

Decisions are:

- automated

- enforced

- logged

- auditable

This is how data quality works in real production systems.

---

## 🔚 Final Note

This repository is intentionally complete but minimal.

It favors:

decisions over metrics

systems over scripts

enforcement over observability

That is the point.

---
