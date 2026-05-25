import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "johnson_quaterne_layer_p.json"
SCRIPT = ROOT / "scripts" / "analyze_johnson_quaterne_layer_p.py"


def load_result():
    if not RESULT.exists():
        subprocess.run([sys.executable, str(SCRIPT), "--write"], check=True)
    return json.loads(RESULT.read_text())


def test_durer_sagrada_johnson_replay():
    data = load_result()
    durer = data["durer_sagrada"]
    assert data["johnson_scheme"]["ambient_strata_for_fixed_mask"] == {
        "0": 495,
        "1": 880,
        "2": 396,
        "3": 48,
        "4": 1,
    }
    assert durer["source_h34_johnson_strata"] == {
        "0": 19,
        "1": 50,
        "2": 17,
        "3": 0,
        "4": 0,
    }
    assert durer["source_h34_affine_johnson_strata"] == {
        "0": 8,
        "1": 36,
        "2": 8,
        "3": 0,
        "4": 0,
    }
    assert durer["terminal_decomposition"] == {
        "source_24_incidence_0": 25,
        "source_34_incidence_1": 50,
        "source_44_incidence_2": 21,
    }
    assert durer["terminal_affine_decomposition"] == {
        "source_34_incidence_1": 36
    }


def test_atlas_class_counts_and_phase_p_stop_rule():
    data = load_result()
    assert data["atlas_class_counts"] == {
        "exact_v4": 144,
        "extra32": 32,
        "outside_main": 60,
    }
    for row in data["separation_tests"]:
        assert row["separates_main_176_from_outside_60"] is True
        assert row["separates_exact_144_from_extra_32"] is False
        assert row["separates_all_classes"] is False


def test_exact_and_extra_share_terminal_johnson_signature():
    data = load_result()
    exact = data["atlas_class_summary"]["exact_v4"]["field_summaries"]
    extra = data["atlas_class_summary"]["extra32"]["field_summaries"]
    fields = [
        "terminal_decomposition",
        "terminal_affine_decomposition",
        "terminal_inner_profile",
        "terminal_affine_inner_profile",
    ]
    for field in fields:
        assert exact[field]["signature_count"] == 1
        assert extra[field]["signature_count"] == 1
        assert exact[field]["top"][0]["signature"] == extra[field]["top"][0]["signature"]
