from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_exact_v4_affine_class.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_exact_v4_affine_class", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_exact_v4_affine_equivalence():
    result = audit.build_exact_v4_affine_class_audit()
    assert result["terminal24_pair_count"] == 236
    assert result["selected_mask_affine_pair_count"] == 176
    assert result["high_plane_selected_values_pair_count"] == 176
    assert result["affine_cell_labeling_pair_count"] == 144
    assert result["exact_canonical_v4_pair_count"] == 144
    assert result["exact_canonical_v4_equals_affine_cell_labeling"] is True
    assert result["selected_mask_affine_equals_selected_values_11_12_15_16"] is True
    assert result["exact_canonical_v4_equals_selected_mask_affine_and_cell_affine"] is True


def test_phase_j_minimal_filter_ladder():
    result = audit.build_exact_v4_affine_class_audit()
    assert result["phase_j_minimal_filter_ladder"] == {
        "terminal24": 236,
        "selected_values_11_12_15_16_or_selected_mask_affine": 176,
        "plus_affine_cell_value_labeling": 144,
        "exact_canonical_v4": 144,
    }
    assert result["main_176_split_by_cell_labeling"] == {
        "cell_affine_exact_v4": 144,
        "cell_non_affine_non_exact": 32,
    }


def test_selected_affine_extras_are_the_known_terminal_sets():
    result = audit.build_exact_v4_affine_class_audit()
    assert result["selected_affine_non_cell_affine_extra_count"] == 32
    assert result["selected_affine_non_cell_affine_terminal_sets"] == {
        "0123,0213,3120,3210": 8,
        "0123,1302,2031,3210": 8,
        "0123,3210": 16,
    }


def test_orientation_free_reading_guardrail():
    result = audit.build_exact_v4_affine_class_audit()
    assert result["orientation_free_reading"] == {
        "affine_cell_value_criterion_stable_under_d4": True,
        "affine_cell_value_criterion_stable_under_complement": True,
        "terminal24_pair_f2_profiles_stable_under_d4": True,
        "canonical_v4_wording_orientation_free": False,
    }
