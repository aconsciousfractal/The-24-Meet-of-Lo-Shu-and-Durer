from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_s4_chambers.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_s4_chambers", SCRIPT)
s4 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(s4)


def test_s4_chamber_fingerprint_group_data():
    result = s4.build_s4_chamber_fingerprints()
    assert result["s4_size"] == 24
    assert result["s4_chamber_edge_count"] == 36
    d4 = result["subsets"]["D4"]
    v4 = result["subsets"]["V4"]
    assert d4["size"] == 8
    assert v4["size"] == 4
    assert d4["is_subgroup"] is True
    assert v4["is_subgroup"] is True
    assert d4["order_profile"] == {"1": 1, "2": 5, "4": 2}
    assert v4["order_profile"] == {"1": 1, "2": 3}
    assert d4["left_coset_count"] == 3
    assert v4["left_coset_count"] == 6


def test_s4_chamber_fingerprint_poset_scope():
    result = s4.build_s4_chamber_fingerprints()
    d4 = result["subsets"]["D4"]
    v4 = result["subsets"]["V4"]
    assert d4["common_precedence_relations"] == []
    assert v4["common_precedence_relations"] == []
    assert d4["common_halfspace_closure_size"] == 24
    assert v4["common_halfspace_closure_size"] == 24
    assert d4["is_standard_poset_cone"] is False
    assert v4["is_standard_poset_cone"] is False


def test_s4_chamber_fingerprint_connectivity():
    result = s4.build_s4_chamber_fingerprints()
    d4_graph = result["subsets"]["D4"]["chamber_graph"]
    v4_graph = result["subsets"]["V4"]["chamber_graph"]
    assert d4_graph["component_count"] == 4
    assert d4_graph["component_sizes"] == [2, 2, 2, 2]
    assert d4_graph["internal_edge_count"] == 4
    assert d4_graph["boundary_edge_count"] == 16
    assert v4_graph["component_count"] == 4
    assert v4_graph["component_sizes"] == [1, 1, 1, 1]
    assert v4_graph["internal_edge_count"] == 0
    assert v4_graph["boundary_edge_count"] == 12
