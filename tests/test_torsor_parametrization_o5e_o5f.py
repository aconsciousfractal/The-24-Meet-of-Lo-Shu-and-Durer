from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_torsor_parametrization_o5e_o5f.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location(
    "analyze_torsor_parametrization_o5e_o5f", SCRIPT
)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_coarse_p_w_fibers_have_size_24():
    result = audit.build_torsor_parametrization_o5e_o5f()
    assert result["affine_square_mask_pair_count"] == 3456
    assert result["fiber_count_by_selected_plane_and_direction"] == 144
    assert result["fiber_size_distribution"] == {"24": 144}
    assert result["full_affine_map_count_per_plane_distribution"] == {"24": 144}


def test_naive_p_w_phi_parametrization_fails():
    result = audit.build_torsor_parametrization_o5e_o5f()
    assert result["naive_p_w_phi_parametrization_holds"] is False
    assert result["distinct_point_map_count_distribution"] == {
        "16": 32,
        "20": 16,
        "24": 96,
    }
    assert result["agl_torsor_fiber_distribution"] == {
        "False": 48,
        "True": 96,
    }
    assert result["agl_torsor_holds_for_all_fibers"] is False


def test_mask_refined_parametrization_is_injective():
    result = audit.build_torsor_parametrization_o5e_o5f()
    assert result["point_map_mask_pair_count_distribution"] == {"24": 144}
    assert result["mask_refined_p_w_phi_mask_parametrization_holds"] is True
    assert result["global_refined_key_count"] == 3456
