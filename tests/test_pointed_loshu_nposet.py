from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_pointed_loshu_nposet.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_pointed_loshu_nposet", SCRIPT)
bridge = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bridge)


def test_unpointed_loshu_graph_does_not_match_n_poset_graph():
    result = bridge.build_pointed_loshu_nposet_analysis()
    assert result["comparisons"]["natural_loshu_isomorphic_to_n_poset_graph"] is False
    assert result["natural_loshu_graph"]["degree_sequence"] == [1, 1, 1, 1, 4]
    assert result["n_poset"]["linear_extension_graph"]["degree_sequence"] == [1, 2, 2, 2, 3]


def test_pointed_loshu_graph_matches_n_poset_and_a2_graphs():
    result = bridge.build_pointed_loshu_nposet_analysis()
    comparisons = result["comparisons"]
    assert comparisons["pointed_loshu_isomorphic_to_n_poset_graph"] is True
    assert comparisons["pointed_loshu_isomorphic_to_a2_ideal_graph"] is True
    assert comparisons["n_poset_graph_isomorphic_to_a2_ideal_graph"] is True
    assert comparisons["explicit_loshu_to_n_mapping_verified"] is True
    assert comparisons["explicit_loshu_to_a2_mapping_verified"] is True


def test_n_poset_linear_extension_graph_is_stable():
    result = bridge.build_pointed_loshu_nposet_analysis()
    assert result["n_poset"]["linear_extensions"] == [
        "acbd",
        "acdb",
        "cabd",
        "cadb",
        "cdab",
    ]
    assert result["n_poset"]["linear_extension_graph"]["edges"] == [
        ["acbd", "acdb"],
        ["acbd", "cabd"],
        ["acdb", "cadb"],
        ["cabd", "cadb"],
        ["cadb", "cdab"],
    ]


def test_boundary_mark_choice_is_isomorphic_but_not_canonical():
    result = bridge.build_pointed_loshu_nposet_analysis()
    assert result["boundary_mark_count"] == 4
    assert result["all_boundary_marks_give_isomorphic_graphs"] is True
    for row in result["pointed_boundary_mark_variants"].values():
        assert row["graph"]["degree_sequence"] == [1, 2, 2, 2, 3]
