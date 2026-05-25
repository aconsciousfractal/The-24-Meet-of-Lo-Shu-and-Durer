from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_six_of_nine_o5c.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_six_of_nine_o5c", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_balanced_complements_split_as_six_invertible_plus_three_rank_one():
    result = audit.build_six_of_nine_o5c()
    assert result["selected_direction"] == [0, 1, 4, 5]
    assert result["coordinate_partner_direction"] == [0, 2, 8, 10]
    assert result["balanced_complement_count"] == 9
    assert result["balanced_complement_graph_rank_distribution"] == {
        "1": 3,
        "2": 6,
    }
    assert result["balanced_complement_is_partner_complement_distribution"] == {
        "False": 3,
        "True": 6,
    }
    assert result["invertible_graph_complement_count"] == 6
    assert result["rank_one_balanced_complement_count"] == 3


def test_terminal24_uses_exactly_the_invertible_graph_complements():
    result = audit.build_six_of_nine_o5c()
    assert result["terminal24_affine_record_count"] == 144
    assert result["terminal_direction_count"] == 6
    assert set(result["terminal_direction_distribution"].values()) == {24}
    assert result["terminal_direction_graph_rank_distribution"] == {"2": 144}
    assert result["terminal_direction_is_partner_complement_distribution"] == {
        "True": 144
    }
    assert result["terminal_direction_is_invertible_graph_distribution"] == {
        "True": 144
    }
    assert result["used_directions_equal_invertible_complements"] is True


def test_unused_balanced_complements_are_the_three_rank_one_graphs():
    result = audit.build_six_of_nine_o5c()
    assert result["unused_balanced_complements"] == [
        [0, 2, 13, 15],
        [0, 7, 8, 15],
        [0, 7, 10, 13],
    ]
    unused = {
        tuple(entry["direction"]): entry
        for entry in result["balanced_complement_details"]
        if entry["direction"] in result["unused_balanced_complements"]
    }
    assert {entry["graph_rank"] for entry in unused.values()} == {1}
    assert {
        entry["complementary_to_partner_direction"] for entry in unused.values()
    } == {False}
