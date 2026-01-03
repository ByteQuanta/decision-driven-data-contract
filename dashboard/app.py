from dashboard.state import SystemState


def render_kv(label: str, value):
    print(f"{label:<25}: {value}")


def main():
    state = SystemState()

    print("\n" + "=" * 50)
    print("      DATA CONTRACT — SYSTEM DASHBOARD")
    print("=" * 50)

    # --- System health ---
    health = state.system_health()
    health_icon = {
        "GREEN": "🟢",
        "YELLOW": "🟡",
        "RED": "🔴",
    }.get(health, "❔")

    print(f"\nSYSTEM HEALTH: {health_icon} {health}\n")

    # --- High-level stats ---
    render_kv("Total events (24h)", state.total_events())
    render_kv("Decision counts", state.decision_counts())
    render_kv("Severity counts", state.severity_counts())

    # --- Latest decision ---
    latest = state.latest_decision()
    print("\nLATEST DECISION")
    print("-" * 50)

    if latest:
        render_kv("Timestamp", latest["timestamp"])
        render_kv("Decision", latest["decision"])
        render_kv("Severity", latest["severity"])
        render_kv("Reason", latest["reason"])
        render_kv("Source file", latest["source_file"])
        render_kv("Row count", latest["row_count"])
    else:
        print("No decisions recorded yet.")

    # --- Frequent problems ---
    print("\nMOST FREQUENT ISSUES (24h)")
    print("-" * 50)

    issues = state.frequent_reasons()
    if issues:
        for reason, count in issues.items():
            print(f"- {reason} ({count}x)")
    else:
        print("No issues detected.")

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
