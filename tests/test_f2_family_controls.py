from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_f2_family_controls.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_f2_family_controls", SCRIPT)
controls = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(controls)


def test_associated_and_most_perfect_have_same_terminal24_f2_profile():
    result = controls.build_f2_family_controls()
    assert result["associated_vs_panmagic_control"]["same_terminal24_f2_profile"] is True

    associated = result["family_summaries"]["associated"]
    most_perfect = result["family_summaries"]["most_perfect_proxy"]
    for summary in (associated, most_perfect):
        assert summary["square_count"] == 48
        assert summary["affine_cell_labeling_square_count"] == 48
        assert summary["terminal24_pair_count"] == 16
        assert summary["terminal24_affine_cell_labeling_pair_count"] == 16
        assert summary["terminal24_selected_mask_affine_pair_count"] == 16
        assert summary["terminal24_exact_canonical_v4_pair_count"] == 16
        assert summary["terminal24_pure_transport_pair_count"] == 16
        assert summary["terminal_affine_count_distribution"] == {"36": 16}
        assert summary["selected_value_signature_counts"] == {"(11, 12, 15, 16)": 16}
        assert summary["selected_mask_direction_counts"] == {"(0, 1, 4, 5)": 16}


def test_complement_fixed_family_has_mixed_f2_profile():
    result = controls.build_f2_family_controls()
    complement_fixed = result["family_summaries"]["complement_fixed"]
    assert complement_fixed["square_count"] == 352
    assert complement_fixed["affine_cell_labeling_square_count"] == 144
    assert complement_fixed["terminal24_pair_count"] == 84
    assert complement_fixed["terminal24_affine_cell_labeling_pair_count"] == 48
    assert complement_fixed["terminal24_selected_mask_affine_pair_count"] == 56
    assert complement_fixed["terminal24_exact_canonical_v4_pair_count"] == 48
    assert complement_fixed["terminal24_pure_transport_pair_count"] == 60
    assert complement_fixed["terminal_affine_count_distribution"] == {
        "30": 4,
        "31": 4,
        "32": 16,
        "35": 4,
        "36": 56,
    }
