from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_order4_f2_extension.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_order4_f2_extension", SCRIPT)
f2ext = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(f2ext)


def test_terminal24_f2_extension_counts():
    result = f2ext.build_order4_f2_extension()
    assert result["all_880_square_cell_labeling_affine_counts"] == {
        "affine_automorphism": 432,
        "non_affine": 448,
    }
    assert result["terminal24_pair_count"] == 236
    assert result["exact_canonical_v4_pair_count"] == 144
    assert result["terminal24_affine_cell_labeling_pair_count"] == 144
    assert result["affine_cell_labeling_pairs_equal_exact_canonical_v4"] is True
    assert result["selected_mask_affine_counts"] == {
        "affine_plane": 176,
        "non_affine": 60,
    }
    assert result["selected_mask_direction_counts"] == {"(0, 1, 4, 5)": 176}


def test_exact_canonical_v4_has_uniform_f2_pure_transport_profile():
    result = f2ext.build_order4_f2_extension()
    v4 = result["exact_canonical_v4_summary"]
    assert v4["pair_count"] == 144
    assert v4["all_cell_labelings_are_affine_automorphisms"] is True
    assert v4["all_selected_masks_are_affine_planes"] is True
    assert v4["selected_mask_direction_counts"] == {"(0, 1, 4, 5)": 144}
    assert v4["all_terminal_affine_layers_are_pure_transport"] is True
    assert v4["terminal_affine_count_distribution"] == {"36": 144}
    assert v4["transported_affine_count_distribution"] == {"36": 144}


def test_selected_value_signature_f2_profiles():
    result = f2ext.build_order4_f2_extension()
    profiles = {
        row["sorted_values"]: row
        for row in result["selected_value_signature_f2_profiles"]
    }
    assert profiles["11,12,15,16"] == {
        "sorted_values": "11,12,15,16",
        "selected_mask_is_affine_plane": True,
        "terminal_count": 96,
        "terminal_affine_count": 36,
        "transported_source34_incidence1_affine_count": 36,
        "terminal_affine_is_pure_transport": True,
        "pair_count": 176,
    }
    assert profiles["11,13,14,15"]["terminal_affine_is_pure_transport"] is True
    assert profiles["11,13,14,15"]["terminal_affine_count"] == 30
    assert profiles["11,13,15,16"]["terminal_affine_is_pure_transport"] is False
