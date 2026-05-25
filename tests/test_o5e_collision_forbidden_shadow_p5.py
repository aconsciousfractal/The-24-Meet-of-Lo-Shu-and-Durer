import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "o5e_collision_forbidden_shadow_p5.json"
SCRIPT = ROOT / "scripts" / "analyze_o5e_collision_and_forbidden_shadow_p5.py"


def load_result():
    if not RESULT.exists():
        subprocess.run([sys.executable, str(SCRIPT), "--write"], check=True)
    return json.loads(RESULT.read_text())


def test_p5_o5e_collision_matching_table():
    data = load_result()
    collision = data["o5e_collision_table"]
    assert collision["fiber_count"] == 144
    assert collision["direction_pair_count"] == 36
    assert collision["distinct_point_map_distribution"] == {
        "16": 32,
        "20": 16,
        "24": 96,
    }
    assert collision["collision_edge_distribution"] == {
        "0": 96,
        "4": 16,
        "8": 32,
    }
    assert collision["max_multiplicity_distribution"] == {
        "1": 96,
        "2": 48,
    }
    assert collision["matching_collision_graph_holds"] is True
    assert collision["direction_pair_classifier_holds"] is True
    assert collision["ambiguous_direction_pairs"] == {}


def test_p5_forbidden_shadow_ambient_domain_planes():
    data = load_result()
    forbidden = data["forbidden_shadow_obstruction"]
    assert forbidden["ambient_domain_affine_plane_count"] == 140
    assert forbidden["ambient_domain_affine_shadow_profile"] == {
        "1,1,1,1": 64,
        "2,2,0,0": 72,
        "4,0,0,0": 4,
    }
    assert forbidden["ambient_has_forbidden_2110"] is False


def test_p5_forbidden_shadow_classifies_main_176():
    data = load_result()
    forbidden = data["forbidden_shadow_obstruction"]
    assert forbidden["main_176_count"] == 176
    assert forbidden["exact_v4_iff_F_2110_zero_inside_main_176"] is True
    assert forbidden["F_2110_equals_non_domain_affine_inside_main_176"] is True
    assert forbidden["invariant_rows_main_176"] == [
        {
            "class": "exact_v4",
            "F_1111": 12,
            "F_2200": 20,
            "F_4000": 4,
            "F_2110": 0,
            "non_domain_affine": 0,
            "count": 144,
        },
        {
            "class": "extra32",
            "F_1111": 12,
            "F_2200": 8,
            "F_4000": 0,
            "F_2110": 16,
            "non_domain_affine": 16,
            "count": 16,
        },
        {
            "class": "extra32",
            "F_1111": 16,
            "F_2200": 8,
            "F_4000": 0,
            "F_2110": 12,
            "non_domain_affine": 12,
            "count": 16,
        },
    ]
