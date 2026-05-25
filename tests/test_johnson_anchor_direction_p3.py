import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "johnson_anchor_direction_p3.json"
SCRIPT = ROOT / "scripts" / "analyze_johnson_anchor_direction_p3.py"


def load_result():
    if not RESULT.exists():
        subprocess.run([sys.executable, str(SCRIPT), "--write"], check=True)
    return json.loads(RESULT.read_text())


def test_p3_class_counts_and_separation():
    data = load_result()
    assert data["class_counts"] == {
        "exact_v4": 144,
        "extra32": 32,
        "outside_main": 60,
    }
    assert data["summary"]["signature_counts"] == {
        "exact_v4": 1,
        "extra32": 2,
        "outside_main": 10,
    }
    assert data["summary"]["pairwise_intersections"] == {
        "exact_v4__extra32": 0,
        "exact_v4__outside_main": 0,
        "extra32__outside_main": 0,
    }


def test_p3_exact_v4_direction_inventory():
    data = load_result()
    exact = data["summary"]["top_by_class"]["exact_v4"][0]
    assert exact == {
        "count": 144,
        "signature": {
            "direction_relation_counts": {
                "complement": 3,
                "line": 5,
                "same": 1,
            },
            "non_domain_affine": 0,
            "quad_relation_counts": {
                "complement": 12,
                "line": 20,
                "same": 4,
            },
        },
    }


def test_p3_extras_do_not_share_exact_direction_inventory():
    data = load_result()
    exact_signature = data["summary"]["top_by_class"]["exact_v4"][0]["signature"]
    for row in data["summary"]["top_by_class"]["extra32"]:
        assert row["signature"] != exact_signature
        assert row["signature"]["non_domain_affine"] > 0
