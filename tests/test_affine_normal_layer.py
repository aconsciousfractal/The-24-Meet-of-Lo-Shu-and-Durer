from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_affine_normal_layer.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_affine_normal_layer", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_affine_layer_counts_and_uniformity():
    result = audit.build_affine_normal_layer()
    assert result["essential_square_count"] == 880
    assert result["affine_square_count"] == 432
    assert result["non_affine_square_count"] == 448
    assert result["affine_square_mask_pair_count"] == 3456
    assert result["selected_value_plane_count"] == 24
    assert result["selected_value_plane_count_distribution"] == {"144": 24}
    assert result["selected_direction_count"] == 6
    assert result["selected_direction_count_distribution"] == {"576": 6}
    assert result["uniformity_reading"][
        "all_selected_value_planes_have_144_pairs"
    ]
    assert result["uniformity_reading"][
        "six_selected_directions_have_576_pairs_each"
    ]


def test_endpoint24_is_one_affine_value_plane():
    result = audit.build_affine_normal_layer()
    assert result["terminal24_affine_layer_pair_count"] == 144
    assert result["terminal24_selected_value_planes"] == {
        "11,12,15,16": 144
    }
    assert result["terminal24_terminal_sets"] == {
        "0123,1032,2301,3210": 144
    }
    assert result["terminal24_all_full_translation_v4"] is True
    assert result["uniformity_reading"][
        "terminal24_is_single_selected_value_plane"
    ]
    assert result["uniformity_reading"][
        "terminal24_in_affine_layer_is_exactly_full_translation_v4"
    ]


def test_affine_endpoint_distribution():
    result = audit.build_affine_normal_layer()
    assert result["endpoint_distribution_affine_layer"] == {
        "22": 144,
        "24": 144,
        "25": 144,
        "26": 432,
        "28": 144,
        "29": 144,
        "30": 432,
        "31": 144,
        "32": 432,
        "33": 432,
        "34": 864,
    }
