from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "fixed_sum24_polytope_audit.json"


def load_result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_fixed_sum24_full_polytope_vertex_counts():
    result = load_result()
    polytope = result["polytope"]
    assert polytope["affine_dimension"] == 7
    assert polytope["vertex_count"] == 292
    assert polytope["integral_vertex_count"] == 180
    assert polytope["semi_integral_vertex_count"] == 112
    assert polytope["max_denominator_distribution"] == {"1": 180, "2": 112}
    assert polytope["active_bound_count_distribution"] == {
        "7": 48,
        "8": 124,
        "9": 80,
        "10": 16,
        "12": 24,
    }


def test_fixed_sum24_full_polytope_symmetry_and_d10():
    result = load_result()
    assert result["polytope"]["D4_square_symmetry_stabilizer"] == [
        "id",
        "rot90",
        "rot180",
        "rot270",
        "ref_main_diag",
        "ref_anti_diag",
        "ref_vertical",
        "ref_horizontal",
    ]
    assert result["polytope"]["D4_square_symmetry_stabilizer_size"] == 8
    assert result["D10"]["is_vertex"] is False
    assert result["D10"]["minimal_face_vertex_count"] == 47
    assert result["D10"]["minimal_face_is_subset_of_full_polytope_vertices"] is True
    assert result["D10"]["local_barycentric_vertex_indices"] == [34, 41]
    assert result["D10"]["barycentric_weights"] == ["4/5", "1/5"]


def test_fixed_sum24_enumeration_audit_counts():
    result = load_result()
    assert result["enumeration"]["bound_hyperplane_count"] == 32
    assert result["enumeration"]["checked_combinations"] == 3365856
    assert result["enumeration"]["float_feasible_combinations"] == 12960
    assert result["enumeration"]["exact_feasible_combinations"] == 12960
