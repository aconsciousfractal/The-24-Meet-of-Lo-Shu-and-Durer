from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_f2_tesseract.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_f2_tesseract", SCRIPT)
f2 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(f2)


def test_durer_value_labeling_is_linear_tesseract_automorphism():
    result = f2.build_f2_tesseract_analysis()
    linear = result["linear_coordination_layer"]
    assert linear["matrix_rank_over_f2"] == 4
    assert linear["is_linear_automorphism"] is True
    assert linear["all_cells_match_formula"] is True
    assert linear["formulas_over_f2"] == [
        "l0 = r1 + c0 + c1",
        "l1 = r0 + c0 + c1",
        "l2 = r0 + r1 + c0",
        "l3 = r0 + r1 + c1",
    ]
    assert linear["all_24_permutation_diagonals_are_affine_planes"] is True


def test_one_incidence_masks_are_affine_planes_but_sagrada_is_terminal_unique():
    result = f2.build_f2_tesseract_analysis()
    masks = result["mask_layer"]
    assert masks["one_incidence_count"] == 8
    assert masks["all_one_incidence_masks_are_affine_planes"] is True
    assert masks["terminal_24_affine_plane_masks"] == ["2013"]


def test_durer_quaterne_affine_splits():
    result = f2.build_f2_tesseract_analysis()
    quaternes = result["quaterne_layer"]
    assert quaternes["ambient_four_cell_sets"] == 1820
    assert quaternes["ambient_affine_planes"] == 140
    assert quaternes["h34_count"] == 86
    assert quaternes["h34_affine_split"] == {"affine": 52, "non_affine": 34}
    assert quaternes["transported_h34_incidence1_affine_split"] == {
        "affine": 36,
        "non_affine": 14,
    }
    assert quaternes["d10_h24_count"] == 96
    assert quaternes["d10_h24_affine_split"] == {"affine": 36, "non_affine": 60}
    assert quaternes["d10_h24_affine_planes_are_exactly_transported_h34_incidence1"] is True


def test_balanced_directions_explain_affine_quaterne_counts():
    result = f2.build_f2_tesseract_analysis()
    directions = result["affine_direction_layer"]
    assert directions["two_dimensional_direction_count"] == 35
    assert directions["affine_plane_count_from_direction_cosets"] == 140
    assert directions["direction_cosets_equal_ambient_affine_planes"] is True
    assert directions["balanced_direction_count"] == 13
    assert directions["balanced_coset_count"] == 52
    assert directions["balanced_cosets_equal_h34_affine_planes"] is True
    assert directions["sagrada_direction"] == [0, 1, 4, 5]
    assert directions["sagrada_direction_is_balanced"] is False
    assert directions["balanced_direction_relation_to_sagrada"] == {
        "complementary_to_sagrada_direction": 9,
        "line_intersection_with_sagrada_direction": 4,
    }
    assert directions["balanced_coset_incidence_by_relation"] == {
        "complementary_to_sagrada_direction_1": 36,
        "line_intersection_with_sagrada_direction_0": 8,
        "line_intersection_with_sagrada_direction_2": 8,
    }
    assert directions["terminal_affine_planes_equal_complementary_balanced_cosets"] is True


def test_diagonal_break_as_affine_maps_over_f2_square():
    result = f2.build_f2_tesseract_analysis()
    diagonal = result["diagonal_affine_layer"]
    assert diagonal["source_D4"]["family_counts"] == {
        "bit_swap_linear_part_translation": 4,
        "identity_linear_part_translation": 4,
    }
    assert diagonal["source_D4"]["is_union_of_translation_and_bit_swap_translation_families"] is True
    assert diagonal["terminal_V4"]["family_counts"] == {
        "identity_linear_part_translation": 4
    }
    assert diagonal["terminal_V4"]["is_translation_subgroup"] is True
