import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "johnson_anchor_refinement_p2.json"
SCRIPT = ROOT / "scripts" / "analyze_johnson_anchor_refinement_p2.py"


def load_result():
    if not RESULT.exists():
        subprocess.run([sys.executable, str(SCRIPT), "--write"], check=True)
    return json.loads(RESULT.read_text())


def test_p2_class_counts_and_terminal_set_sizes():
    data = load_result()
    assert data["class_counts"] == {
        "exact_v4": 144,
        "extra32": 32,
        "outside_main": 60,
    }
    assert data["terminal_set_size_by_class"]["exact_v4"] == {"4": 144}
    assert data["terminal_set_size_by_class"]["extra32"] == {"2": 16, "4": 16}


def test_fixed_translation_anchor_separates_144_32_and_outside():
    data = load_result()
    summaries = {
        row["field"]: row
        for row in data["profile_summaries"]
    }
    for field in (
        "fixed_translation_terminal_anchor_profile",
        "fixed_translation_terminal_affine_anchor_profile",
    ):
        row = summaries[field]
        assert row["pairwise_intersections"] == {
            "exact_v4__extra32": 0,
            "exact_v4__outside_main": 0,
            "extra32__outside_main": 0,
        }
        assert row["separates_exact_144_from_extra_32"] is True
        assert row["separates_all_classes"] is True


def test_exact_v4_fixed_anchor_signature_is_uniform():
    data = load_result()
    summaries = {
        row["field"]: row
        for row in data["profile_summaries"]
    }
    terminal = summaries["fixed_translation_terminal_anchor_profile"]
    affine = summaries["fixed_translation_terminal_affine_anchor_profile"]
    assert terminal["signature_counts"]["exact_v4"] == 1
    assert terminal["top_by_class"]["exact_v4"][0] == {
        "count": 144,
        "signature": {
            "1,1,1,1": 16,
            "2,1,1,0": 48,
            "2,2,0,0": 20,
            "3,1,0,0": 8,
            "4,0,0,0": 4,
        },
    }
    assert affine["top_by_class"]["exact_v4"][0] == {
        "count": 144,
        "signature": {
            "1,1,1,1": 12,
            "2,2,0,0": 20,
            "4,0,0,0": 4,
        },
    }
