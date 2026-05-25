from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_terminal_parallel_torsor_o5b.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location(
    "analyze_terminal_parallel_torsor_o5b", SCRIPT
)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def assert_torsor_summary(summary: dict, expected_count: int) -> None:
    assert summary["record_count"] == expected_count
    assert summary["translation_direction_balanced_distribution"] == {
        "True": expected_count
    }
    assert summary["translation_direction_complementary_to_selected_distribution"] == {
        "True": expected_count
    }
    assert summary["translation_transversal_intersection_distribution"] == {
        "(1, 1, 1, 1)": expected_count
    }
    assert summary["translation_to_selected_point_map_bijection_distribution"] == {
        "True": expected_count
    }
    assert summary["translation_to_selected_point_map_affine_distribution"] == {
        "True": expected_count
    }


def test_fixed_translation_torsor_holds_on_full_affine_layer():
    result = audit.build_terminal_parallel_torsor_o5b()
    assert_torsor_summary(result["all_affine_translation_torsor_summary"], 3456)


def test_terminal_torsor_holds_on_full_translation_subclass():
    result = audit.build_terminal_parallel_torsor_o5b()
    assert_torsor_summary(result["full_translation_terminal_torsor_summary"], 1968)


def test_terminal24_exact_v4_torsor_refinement():
    result = audit.build_terminal_parallel_torsor_o5b()
    assert result["terminal24_affine_record_count"] == 144
    assert result["selected_direction_distribution"] == {"0,1,4,5": 144}
    assert result["balanced_complements_to_selected_direction_count_distribution"] == {
        "9": 144
    }
    assert set(result["terminal_direction_distribution"].values()) == {24}
    assert len(result["terminal_direction_distribution"]) == 6
    assert result["terminal_direction_balanced_distribution"] == {"True": 144}
    assert result["terminal_direction_complementary_to_selected_distribution"] == {
        "True": 144
    }
    assert result["terminal_to_selected_point_map_bijection_distribution"] == {
        "True": 144
    }
    assert result["terminal_to_selected_point_map_affine_distribution"] == {
        "True": 144
    }


def test_value_bit_kernel_still_does_not_act_as_terminal_v4():
    result = audit.build_terminal_parallel_torsor_o5b()
    assert result["kernel_setwise_stabilizer_size_distribution"] == {"2": 144}
    assert result["kernel_setwise_point_orbit_size_distribution"] == {
        "(1, 1, 2)": 144
    }
    assert result["kernel_full_selected_plane_orbit_size_distribution"] == {
        "2": 144
    }
