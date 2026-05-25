from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_bounded_magic_polytope.py"

spec = importlib.util.spec_from_file_location("bounded_magic_polytope", SCRIPT)
poly = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(poly)


def test_magic_affine_space_dimensions():
    assert poly.affine_space_summary(3) == {
        "n": 3,
        "variable_count": 9,
        "line_count": 8,
        "free_sum_rank": 6,
        "free_sum_dimension": 3,
        "fixed_sum_rank": 7,
        "fixed_sum_dimension": 2,
    }
    assert poly.affine_space_summary(4) == {
        "n": 4,
        "variable_count": 16,
        "line_count": 10,
        "free_sum_rank": 8,
        "free_sum_dimension": 8,
        "fixed_sum_rank": 9,
        "fixed_sum_dimension": 7,
    }


def test_sagrada_ray_terminal_face_data():
    ray = poly.sagrada_ray_summary()
    assert ray["mask"] == "2013"
    assert ray["t_interval_downward"] == [0, 10]
    assert ray["source_magic_sum"] == 34
    assert ray["terminal_magic_sum"] == 24
    assert ray["terminal_hit_cells"] == [
        {"cell": [2, 1], "label": "r2c1", "source_value": 11}
    ]
    assert ray["D10"]["free_sum_face"]["is_vertex"] is False
    assert ray["D10"]["fixed_sum_face"]["is_vertex"] is False
    assert ray["D10"]["free_sum_face"]["face_dimension"] == 6
    assert ray["D10"]["fixed_sum_face"]["face_dimension"] == 5


def test_d10_fixed_sum_minimal_face_vertices():
    face = poly.enumerate_fixed_sum_face_vertices()
    assert face["face_dimension"] == 5
    assert face["vertex_count"] == 47
    assert face["integral_vertex_count"] == 37
    assert face["max_denominator_distribution"] == {"1": 37, "2": 10}
    assert face["active_bound_count_distribution"] == {
        "7": 6,
        "8": 19,
        "9": 6,
        "10": 8,
        "12": 8,
    }
    assert face["D10_is_vertex_of_this_face"] is False


def test_d10_local_face_fingerprint():
    fingerprint = poly.local_face_fingerprint()
    assert fingerprint["common_active_bounds_across_vertices"] == [
        {"cell": [0, 0], "label": "r0c0", "value": 1},
        {"cell": [2, 1], "label": "r2c1", "value": 1},
    ]
    assert fingerprint["D4_vertex_set_stabilizer"] == ["id"]
    assert fingerprint["D4_vertex_set_stabilizer_size"] == 1
    assert fingerprint["D10_active_bounds_equal_common_active_bounds"] is True
    assert fingerprint["D10_relative_interior_of_minimal_face"] is True
    assert fingerprint["D10_nonforced_min_lower_slack"] == 1
    assert fingerprint["D10_nonforced_min_upper_slack"] == 2


def test_d10_barycentric_certificate():
    cert = poly.local_face_barycentric_certificate()
    assert cert["type"] == "two_vertex_segment"
    assert cert["vertex_indices"] == [34, 41]
    assert cert["weights"] == ["4/5", "1/5"]
    assert cert["weights_sum"] == 1
    assert cert["strictly_positive_weights"] is True
    assert cert["reconstructs_D10"] is True


def test_sagrada_ray_active_facets():
    ray = poly.sagrada_ray_summary()
    assert [item["label"] for item in ray["active_bounds_along_ray"]["t_0"]] == [
        "r0c0",
        "r3c3",
    ]
    assert [item["label"] for item in ray["active_bounds_along_ray"]["t_1_to_9_constant"]] == [
        "r0c0"
    ]
    assert [item["label"] for item in ray["active_bounds_along_ray"]["t_10"]] == [
        "r0c0",
        "r2c1",
    ]


def test_lo_shu_parametric_s24_fiber():
    lo = poly.lo_shu_parametric_summary()
    assert lo["counts_by_sum"] == {
        "3": 1,
        "6": 5,
        "9": 13,
        "12": 25,
        "15": 41,
        "18": 25,
        "21": 13,
        "24": 5,
        "27": 1,
    }
    assert lo["s24"]["dimension"] == 2
    assert lo["s24"]["lattice_point_count"] == 5
    assert lo["s24"]["common_active_bounds"] == []
    assert lo["s24"]["is_common_boundary_face_of_free_polytope"] is False


def test_lo_shu_lattice_formula():
    formula = poly.lo_shu_lattice_formula_summary()
    assert formula["all_counts_match_formula"] is True
    assert formula["counts_by_sum_formula"] == {
        "3": 1,
        "6": 5,
        "9": 13,
        "12": 25,
        "15": 41,
        "18": 25,
        "21": 13,
        "24": 5,
        "27": 1,
    }
    s24 = [row for row in formula["rows"] if row["sum"] == 24][0]
    assert s24["g"] == 8
    assert s24["m"] == 1
    assert s24["pick_formula_count"] == 5
    assert s24["vertices_ab"] == [[1, 0], [0, 1], [-1, 0], [0, -1]]
