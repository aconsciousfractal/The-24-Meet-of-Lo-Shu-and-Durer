from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "magic24_certificates.py"

spec = importlib.util.spec_from_file_location("magic24_certificates", SCRIPT)
magic24 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(magic24)


def test_lo_shu_bounded_counts_and_fibers():
    spectrum = magic24.lo_shu_bounded_spectrum()
    assert spectrum["counts_by_sum"] == {
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
    assert spectrum["upward_spectrum_above_15"] == [18, 21, 24, 27]
    assert len(spectrum["s24_matrices"]) == 5
    assert spectrum["s27_matrices"] == [[[9, 9, 9], [9, 9, 9], [9, 9, 9]]]


def test_durer_one_incidence_masks():
    masks = magic24.durer_one_incidence_masks()
    assert masks["admissible_count"] == 8
    assert masks["terminal_24_masks"] == ["2013"]
    sagrada = [row for row in masks["masks"] if row["perm"] == "2013"][0]
    assert sagrada["values"] == [15, 12, 11, 16]
    assert sagrada["t_max"] == 10
    assert sagrada["terminal_sum"] == 24


def test_durer_pattern_transport():
    transport = magic24.durer_pattern_transport()
    assert transport["h34_count"] == 86
    assert transport["h34_incidence_distribution"] == {"0": 19, "1": 50, "2": 17}
    assert transport["d10_h24_count"] == 96
    assert transport["d10_h24_source_decomposition"] == {
        "source_sum_24_incidence_0": 25,
        "source_sum_34_incidence_1": 50,
        "source_sum_44_incidence_2": 21,
    }


def test_permutation_diagonal_break_and_poset_scope():
    diagonals = magic24.durer_permutation_diagonals()
    assert diagonals["target_diagonals_by_t"]["0"] == [
        "0123",
        "0213",
        "1032",
        "1302",
        "2031",
        "2301",
        "3120",
        "3210",
    ]
    expected_v4 = ["0123", "1032", "2301", "3210"]
    for t in range(1, 11):
        assert diagonals["target_diagonals_by_t"][str(t)] == expected_v4
    assert diagonals["g34_is_subgroup"] is True
    assert diagonals["v4_is_subgroup"] is True
    assert diagonals["g34_order_profile"] == {"1": 1, "2": 5, "4": 2}
    assert diagonals["v4_order_profile"] == {"1": 1, "2": 3}
    assert len(diagonals["g34_left_cosets"]) == 3
    assert len(diagonals["v4_left_cosets"]) == 6
    assert diagonals["poset_cone_tests"]["V4"]["common_precedence_relations"] == []
    assert diagonals["poset_cone_tests"]["V4"]["common_halfspace_closure_size"] == 24
    assert diagonals["poset_cone_tests"]["V4"]["is_standard_poset_cone"] is False


def test_apd_and_centered_determinant_polynomials():
    polys = magic24.centered_ray_polynomials()
    assert polys["apd_coefficients_ascending"]["1"] == [0]
    assert polys["apd_coefficients_ascending"]["2"] == [0]
    assert polys["apd_coefficients_ascending"]["3"] == [0, -1536, 480, -24]
    assert polys["det_ehat_coefficients_ascending"] == [0, -256, 80, -4]
    assert polys["apd3_equals_6_det_ehat"] is True
