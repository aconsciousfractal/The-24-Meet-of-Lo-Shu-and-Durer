from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_affine_normal_spread_structure.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location(
    "analyze_affine_normal_spread_structure", SCRIPT
)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_affine_normal_spread_counts():
    result = audit.build_affine_normal_spread_structure()
    assert result["affine_square_count"] == 432
    assert result["affine_square_mask_pair_count"] == 3456
    assert result["selected_value_plane_count"] == 24
    assert result["selected_value_plane_count_distribution"] == {"144": 24}


def test_each_affine_square_has_two_direction_spread():
    result = audit.build_affine_normal_spread_structure()
    assert result["square_selected_plane_count_distribution"] == {"8": 432}
    assert result["square_selected_direction_count_distribution"] == {"2": 432}
    assert result["all_squares_have_eight_planes_and_two_directions"]


def test_three_coordinate_axis_matchings():
    result = audit.build_affine_normal_spread_structure()
    assert result["coordinate_axis_matching_count"] == 3
    assert result["coordinate_axis_matching_distribution"] == {
        "1,2 | 4,8": 144,
        "1,4 | 2,8": 144,
        "1,8 | 2,4": 144,
    }
    assert result["plane_set_count"] == 3
    assert result["plane_set_count_distribution"] == {"144": 3}
    assert result["all_matchings_have_144_squares"]
    assert result["all_matching_planes_have_144_pairs"]


def test_value_bit_action_explains_equal_matching_sizes():
    result = audit.build_affine_normal_spread_structure()
    action = result["value_bit_matching_action"]
    assert action["value_bit_permutation_count"] == 24
    assert action["affine_layer_preserving_value_bit_permutations"] == 24
    assert action["all_value_bit_permutations_preserve_affine_layer"]
    assert action["induced_matching_action_count"] == 6
    assert action["induced_matching_action_preimage_distribution"] == {"4": 6}
    assert action["matching_stabilizer_sizes"] == {
        "1,2 | 4,8": 8,
        "1,4 | 2,8": 8,
        "1,8 | 2,4": 8,
    }


def test_terminal24_plane_in_matching_layer():
    result = audit.build_affine_normal_spread_structure()
    rows = {
        row["coordinate_axis_matching"]: row for row in result["matching_summaries"]
    }
    matching = rows["1,4 | 2,8"]
    planes = {
        row["selected_values"]: row["pair_count"]
        for row in matching["selected_planes"]
    }
    assert planes["11,12,15,16"] == 144
    assert matching["endpoint_distribution"]["24"] == 144
