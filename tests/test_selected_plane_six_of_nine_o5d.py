from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_selected_plane_six_of_nine_o5d.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location(
    "analyze_selected_plane_six_of_nine_o5d", SCRIPT
)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_six_of_nine_holds_for_all_selected_planes():
    result = audit.build_selected_plane_six_of_nine_o5d()
    assert result["affine_square_mask_pair_count"] == 3456
    assert result["selected_plane_count"] == 24
    assert result["selected_direction_count"] == 6
    assert result["plane_record_count_distribution"] == {"144": 24}
    assert result["all_planes_have_nine_balanced_complements"] is True
    assert (
        result["all_planes_have_six_invertible_and_three_rank_one_complements"]
        is True
    )
    assert result["all_planes_use_exactly_invertible_complements"] is True
    assert result["violation_count"] == 0


def test_each_selected_plane_uses_six_directions_uniformly():
    result = audit.build_selected_plane_six_of_nine_o5d()
    assert result["used_direction_count_per_plane_distribution"] == {"6": 24}
    assert result["used_direction_multiplicity_per_plane_distribution"] == {
        "(24, 24, 24, 24, 24, 24)": 24
    }
    assert result["balanced_complement_rank_split_distribution"] == {
        "(6, 3)": 24
    }


def test_each_selected_direction_has_four_selected_planes():
    result = audit.build_selected_plane_six_of_nine_o5d()
    assert len(result["direction_summaries"]) == 6
    assert all(
        summary["selected_plane_count"] == 4
        and summary["all_planes_use_six_invertible_complements"]
        for summary in result["direction_summaries"]
    )
