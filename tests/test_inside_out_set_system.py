from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_inside_out_set_system.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_inside_out_set_system", SCRIPT)
inside_out = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(inside_out)


def test_inside_out_quaterne_counts_are_stable():
    result = inside_out.build_inside_out_set_system_audit()
    assert result["h34_count"] == 86
    assert result["h24_count"] == 96


def test_magic_lines_and_mask_ranks():
    result = inside_out.build_inside_out_set_system_audit()
    magic_lines = result["system_by_name"]["magic_lines"]
    lines_plus_mask = result["system_by_name"]["lines_plus_mask"]

    assert magic_lines["edge_count"] == 10
    assert magic_lines["rank_over_Q"] == 9
    assert magic_lines["rank_over_F2"] == 8
    assert magic_lines["right_kernel_dimension_over_Q"] == 7
    assert magic_lines["snf"]["nonzero_diagonal_counts"] == {"1": 8, "2": 1}
    assert magic_lines["automorphisms"]["automorphism_group_order"] == 8

    assert lines_plus_mask["edge_count"] == 11
    assert lines_plus_mask["rank_over_Q"] == 10
    assert lines_plus_mask["rank_over_F2"] == 9
    assert lines_plus_mask["right_kernel_dimension_over_Q"] == 6
    assert lines_plus_mask["snf"]["nonzero_diagonal_counts"] == {"1": 9, "2": 1}
    assert lines_plus_mask["automorphisms"]["automorphism_group_order"] == 1


def test_source_terminal_and_combined_systems_are_full_rank_over_q():
    result = inside_out.build_inside_out_set_system_audit()
    expected = {
        "source": {
            "edge_count": 97,
            "left_dependencies": 81,
            "snf": {"1": 14, "2": 1, "40": 1},
        },
        "terminal": {
            "edge_count": 107,
            "left_dependencies": 91,
            "snf": {"1": 14, "2": 1, "20": 1},
        },
        "combined": {
            "edge_count": 193,
            "left_dependencies": 177,
            "snf": {"1": 14, "2": 1, "20": 1},
        },
    }
    for name, values in expected.items():
        system = result["system_by_name"][name]
        assert system["edge_count"] == values["edge_count"]
        assert system["rank_over_Q"] == 16
        assert system["rank_over_F2"] == 14
        assert system["right_kernel_dimension_over_Q"] == 0
        assert system["left_dependency_dimension_over_Q"] == values["left_dependencies"]
        assert system["snf"]["nonzero_diagonal_counts"] == values["snf"]


def test_colored_source_terminal_and_combined_systems_are_rigid():
    result = inside_out.build_inside_out_set_system_audit()
    for name in ("source", "terminal", "combined"):
        system = result["system_by_name"][name]
        assert system["automorphisms"]["automorphism_group_order"] == 1
        assert system["automorphisms"]["cell_orbit_size_distribution"] == {1: 16}


def test_terminal_edge_decomposition_matches_transport_sources():
    result = inside_out.build_inside_out_set_system_audit()
    terminal_colors = result["system_by_name"]["terminal"]["edge_color_counts"]
    assert terminal_colors["h24_source_24_incidence_0"] == 25
    assert terminal_colors["h24_source_34_incidence_1"] == 50
    assert terminal_colors["h24_source_44_incidence_2"] == 21

    source_colors = result["system_by_name"]["source"]["edge_color_counts"]
    assert source_colors["h34_incidence_0"] == 19
    assert source_colors["h34_incidence_1"] == 50
    assert source_colors["h34_incidence_2"] == 17
