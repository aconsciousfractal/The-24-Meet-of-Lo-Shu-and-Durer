import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "johnson_followup_p4.json"
SCRIPT = ROOT / "scripts" / "analyze_johnson_followup_p4.py"


def load_result():
    if not RESULT.exists():
        subprocess.run([sys.executable, str(SCRIPT), "--write"], check=True)
    return json.loads(RESULT.read_text())


def test_p4_terminal24_class_counts_and_affine_signature_counts():
    data = load_result()
    terminal = data["terminal24_code_audit"]
    assert terminal["class_counts"] == {
        "exact_v4": 144,
        "extra32": 32,
        "outside_main": 60,
    }
    affine_summary = {
        row["field"]: row for row in terminal["summaries"]
    }["terminal_affine_profile"]
    assert affine_summary["signature_counts"] == {
        "exact_v4": 1,
        "extra32": 2,
        "outside_main": 12,
    }
    assert affine_summary["pairwise_intersections"] == {
        "exact_v4__extra32": 0,
        "exact_v4__outside_main": 0,
        "extra32__outside_main": 0,
    }


def test_p4_exact_terminal_affine_code_signature():
    data = load_result()
    exact = data["terminal24_code_audit"]["exact_terminal_affine_signature"]
    assert exact["count"] == 36
    assert exact["inner_distribution"] == {"0": 246, "1": 192, "2": 192}
    assert exact["point_degree_profile"] == {"9": 16}
    assert exact["anchor_shadow_profile"] == {
        "1,1,1,1": 12,
        "2,2,0,0": 20,
        "4,0,0,0": 4,
    }
    assert exact["domain_direction_inventory"] == {
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
    }


def test_p4_o5e_collision_refinement():
    data = load_result()
    collision = data["o5e_collision_audit"]
    assert collision["distinct_point_map_count_distribution"] == {
        "16": 32,
        "20": 16,
        "24": 96,
    }
    classifier = collision["joint_selected_direction_translation_direction_classifier"]
    assert classifier["joint_key_count"] == 36
    assert classifier["ambiguous_joint_key_count"] == 0
    assert classifier["ambiguous_joint_keys"] == {}
    assert collision["selected_plane_direction_collision_distribution"] == {
        "0,1,2,3": {"24": 24},
        "0,1,4,5": {"16": 8, "24": 16},
        "0,1,8,9": {"16": 8, "20": 8, "24": 8},
        "0,2,4,6": {"16": 8, "20": 8, "24": 8},
        "0,2,8,10": {"16": 8, "24": 16},
        "0,4,8,12": {"24": 24},
    }
