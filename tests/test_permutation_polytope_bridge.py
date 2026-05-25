from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_permutation_polytope_bridge.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_permutation_polytope_bridge", SCRIPT)
bridge = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bridge)


def test_permutation_polytope_dimensions():
    result = bridge.build_permutation_polytope_bridge()
    assert result["subsets"]["D4"]["permutation_polytope_dimension"] == 5
    assert result["subsets"]["V4"]["permutation_polytope_dimension"] == 3
    assert result["comparison"]["dimension_drop"] == "5 -> 3"


def test_birkhoff_graph_edge_drop():
    result = bridge.build_permutation_polytope_bridge()
    assert result["subsets"]["D4"]["birkhoff_induced_edge_count"] == 16
    assert result["subsets"]["V4"]["birkhoff_induced_edge_count"] == 0
    assert result["subsets"]["V4"]["is_birkhoff_independent_set"] is True
    assert result["comparison"]["birkhoff_edge_drop"] == "16 -> 0"


def test_coset_level_birkhoff_fingerprints():
    result = bridge.build_permutation_polytope_bridge()
    assert len(result["cosets"]["D4"]) == 3
    assert len(result["cosets"]["V4"]) == 6
    assert result["comparison"]["all_d4_cosets_have_same_dimension_and_edge_count"] is True
    assert result["comparison"]["all_v4_cosets_are_birkhoff_independent"] is True
    assert {row["permutation_polytope_dimension"] for row in result["cosets"]["D4"]} == {5}
    assert {row["permutation_polytope_dimension"] for row in result["cosets"]["V4"]} == {3}
