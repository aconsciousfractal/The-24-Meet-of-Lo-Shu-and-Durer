from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_f2_hypergraph_automorphisms.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_f2_hypergraph_automorphisms", SCRIPT)
auto = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(auto)


def test_f2_hypergraph_automorphism_orders():
    result = auto.build_hypergraph_automorphism_audit()
    cases = result["case_by_name"]
    assert cases["H34_all"]["automorphism_group_order"] == 2
    assert cases["H34_affine_colored"]["automorphism_group_order"] == 2
    assert cases["H34_affine_only"]["automorphism_group_order"] == 384
    assert cases["H24_all"]["automorphism_group_order"] == 16
    assert cases["H24_affine_colored"]["automorphism_group_order"] == 2
    assert cases["H24_source_colored"]["automorphism_group_order"] == 1
    assert cases["H24_source_affine_colored"]["automorphism_group_order"] == 1


def test_h34_affine_sublayer_is_transitive_but_full_h34_is_not():
    result = auto.build_hypergraph_automorphism_audit()
    cases = result["case_by_name"]
    assert cases["H34_all"]["cell_orbit_size_distribution"] == {2: 8}
    assert cases["H34_all"]["sagrada_mask_orbit_count"] == 2
    assert cases["H34_affine_only"]["cell_orbit_size_distribution"] == {16: 1}
    assert cases["H34_affine_only"]["sagrada_mask_orbit_count"] == 24
    assert cases["H34_affine_only"]["sagrada_mask_stabilizer_order"] == 16


def test_h24_transport_coloring_is_rigid():
    result = auto.build_hypergraph_automorphism_audit()
    cases = result["case_by_name"]
    assert cases["H24_all"]["cell_orbit_size_distribution"] == {1: 8, 2: 4}
    assert cases["H24_all"]["sagrada_mask_orbit_count"] == 16
    assert cases["H24_affine_colored"]["automorphism_group_order"] == 2
    assert cases["H24_source_colored"]["automorphism_group_order"] == 1
    assert cases["H24_source_affine_colored"]["automorphism_group_order"] == 1
    assert cases["H24_source_colored"]["cell_orbit_size_distribution"] == {1: 16}
