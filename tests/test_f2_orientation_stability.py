from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_f2_orientation_stability.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_f2_orientation_stability", SCRIPT)
stability = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(stability)


def test_d4_domain_transforms_are_affine_automorphisms():
    result = stability.build_orientation_stability_audit()
    assert result["all_d4_domain_transforms_are_affine_automorphisms"] is True
    assert len(result["d4_domain_transform_profiles"]) == 8
    assert all(
        profile["linear_rank_over_f2"] == 4
        for profile in result["d4_domain_transform_profiles"]
    )


def test_affine_cell_value_criterion_is_d4_orientation_stable():
    result = stability.build_orientation_stability_audit()
    assert result["essential_square_count"] == 880
    assert result["orientation_affine_count_distribution"] == {"0": 448, "8": 432}
    assert result["orientation_affine_flag_stable_for_all_880"] is True
    assert result["unstable_orientation_square_indices"] == []
    assert result["raw_oriented_total"] == 7040
    assert result["raw_oriented_affine_cell_labeling_count"] == 3456
    assert result["raw_oriented_non_affine_cell_labeling_count"] == 3584


def test_affine_cell_value_criterion_is_complement_stable():
    result = stability.build_orientation_stability_audit()
    assert result["direct_value_complement_stable_count"] == 880
    assert result["canonical_value_complement_stable_count"] == 880


def test_terminal24_pair_f2_profiles_are_d4_stable():
    result = stability.build_orientation_stability_audit()
    assert result["terminal24_pair_count"] == 236
    assert result["terminal24_pair_d4_profile_stable"] is True
    assert result["unstable_terminal24_records"] == []
