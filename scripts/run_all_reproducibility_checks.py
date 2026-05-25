"""Run the public Magic 24 reproducibility smoke checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    [sys.executable, "scripts/magic24_certificates.py", "--write"],
    [sys.executable, "scripts/analyze_f2_tesseract.py", "--write"],
    [sys.executable, "scripts/analyze_affine_normal_count_derivation.py", "--write"],
    [sys.executable, "scripts/analyze_forbidden_shadow_split_p6.py", "--write"],
    [sys.executable, "-m", "pytest", "-q"],
]


def public_command(cmd: list[str]) -> list[str]:
    if cmd and cmd[0] == sys.executable:
        return ["python", *cmd[1:]]
    return cmd


def main() -> int:
    results = []
    for cmd in COMMANDS:
        print("[run]", " ".join(cmd), flush=True)
        completed = subprocess.run(cmd, cwd=ROOT)
        results.append({"command": public_command(cmd), "returncode": completed.returncode})
        if completed.returncode != 0:
            break

    out = ROOT / "results" / "public_reproducibility_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"commands": results}, indent=2) + "\n", encoding="utf-8")
    print("[wrote]", out)
    return 0 if all(r["returncode"] == 0 for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
