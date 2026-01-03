import json
from datetime import datetime
from pathlib import Path
import shutil


class ActionExecutor:
    def __init__(
        self,
        validated_dir="data/validated",
        rejected_dir="data/rejected",
        decision_log_path="decisions/decision_log.jsonl",
    ):
        self.validated_dir = Path(validated_dir)
        self.rejected_dir = Path(rejected_dir)
        self.decision_log_path = Path(decision_log_path)

        self.validated_dir.mkdir(parents=True, exist_ok=True)
        self.rejected_dir.mkdir(parents=True, exist_ok=True)
        self.decision_log_path.parent.mkdir(parents=True, exist_ok=True)

    def execute(self, decision, df):
        source_file = df.attrs.get("source_file")

        if not source_file:
            raise ValueError("Source file information missing from DataFrame attrs.")

        timestamp = datetime.utcnow().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "decision": decision.name,
            "severity": decision.severity,
            "reason": decision.reason,
            "source_file": source_file,
            "row_count": df.attrs.get("row_count"),
        }

        # ---- Apply action ----
        if decision.name == "ALLOW":
            self._move_file(source_file, self.validated_dir)

        elif decision.name in ("ALLOW_WITH_ALERT", "BLOCK_AND_ROLLBACK"):
            self._move_file(source_file, self.rejected_dir)

        # ---- Write decision log ----
        with open(self.decision_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

        return log_entry

    def _move_file(self, filename, target_dir: Path):
        source_path = Path("data/incoming") / filename
        target_path = target_dir / filename

        if source_path.exists():
            shutil.move(str(source_path), str(target_path))
