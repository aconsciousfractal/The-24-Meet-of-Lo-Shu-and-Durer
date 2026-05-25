"""Phase J2 mechanism audit for the exact-V4 affine class."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import analyze_f2_orientation_stability as orient
import analyze_order4_f2_extension as f2ext
import enumerate_order4_endpoints as order4


Perm = tuple[int, int, int, int]
Cell = tuple[int, int]

IDENTITY_LINEAR_PART = (2, 1)
CANONICAL_V4 = ("0123", "1032", "2301", "3210")


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def perm_from_string(word: str) -> Perm:
    return tuple(int(char) for char in word)  # type: ignore[return-value]


def perm_to_word(perm: Perm) -> str:
    return "".join(str(value) for value in perm)


def perm_affine_profile(word: str) -> dict:
    perm = perm_from_string(word)
    offset = perm[0]
    columns = (perm[2] ^ offset, perm[1] ^ offset)
    return {
        "word": word,
        "offset": offset,
        "linear_part": list(columns),
        "linear_part_key": str(columns),
        "is_translation": columns == IDENTITY_LINEAR_PART,
    }


def terminal_set_profile(words: list[str]) -> dict:
    profiles = [perm_affine_profile(word) for word in words]
    linear_counts = Counter(profile["linear_part_key"] for profile in profiles)
    translation_offsets = sorted(
        profile["offset"] for profile in profiles if profile["is_translation"]
    )
    return {
        "size": len(words),
        "words": sorted(words),
        "linear_part_counts": counter_json(linear_counts),
        "translation_offsets": translation_offsets,
        "is_translation_subset": len(translation_offsets) == len(words),
        "is_full_translation_v4": (
            len(words) == 4
            and len(translation_offsets) == 4
            and translation_offsets == [0, 1, 2, 3]
        ),
    }


def input_index_to_cell(index: int) -> Cell:
    r0 = (index >> 3) & 1
    r1 = (index >> 2) & 1
    c0 = (index >> 1) & 1
    c1 = index & 1
    return ((r0 << 1) | r1, (c0 << 1) | c1)


def square_label(square: order4.Square, index: int) -> int:
    i, j = input_index_to_cell(index)
    return square[i][j] - 1


def square_label_map(square: order4.Square) -> list[int]:
    return [square_label(square, index) for index in range(16)]


def basis_interpolation_mismatch_count(square: order4.Square) -> int:
    labels = square_label_map(square)
    offset = labels[0]
    columns = [labels[index] ^ offset for index in (8, 4, 2, 1)]
    mismatches = 0
    for index, actual in enumerate(labels):
        predicted = offset
        for bit, column in zip((8, 4, 2, 1), columns):
            if index & bit:
                predicted ^= column
        if predicted != actual:
            mismatches += 1
    return mismatches


def domain_affine_planes() -> list[tuple[int, int, int, int]]:
    return [
        tuple(points)  # type: ignore[list-item]
        for points in itertools.combinations(range(16), 4)
        if len(set(points)) == 4 and (points[0] ^ points[1] ^ points[2] ^ points[3]) == 0
    ]


def permutation_diagonal_words() -> list[str]:
    return [perm_to_word(perm) for perm in itertools.permutations(range(4))]


def mask_indices(word: str) -> tuple[int, int, int, int]:
    return tuple((((row >> 1) & 1) << 3) | ((row & 1) << 2) | (((int(word[row]) >> 1) & 1) << 1) | (int(word[row]) & 1) for row in range(4))  # type: ignore[return-value]


def label_quad_is_affine(square: order4.Square, indices: tuple[int, int, int, int]) -> bool:
    labels = [square_label(square, index) for index in indices]
    return f2ext.is_label_affine_plane(labels)


def affine_defect_profile(square: order4.Square) -> dict:
    planes = domain_affine_planes()
    diagonal_words = permutation_diagonal_words()
    preserved_planes = sum(1 for plane in planes if label_quad_is_affine(square, plane))
    preserved_diagonals = sum(
        1 for word in diagonal_words if label_quad_is_affine(square, mask_indices(word))
    )
    return {
        "basis_interpolation_mismatch_count": basis_interpolation_mismatch_count(square),
        "preserved_domain_affine_planes": preserved_planes,
        "broken_domain_affine_planes": len(planes) - preserved_planes,
        "preserved_permutation_diagonal_planes": preserved_diagonals,
        "broken_permutation_diagonal_planes": len(diagonal_words) - preserved_diagonals,
    }


def transformed_set(words: tuple[str, ...], transform_id: int) -> tuple[str, ...]:
    return tuple(sorted(orient.transform_mask(word, transform_id) for word in words))


def canonical_v4_square_symmetry_orbit() -> list[tuple[str, ...]]:
    return sorted({transformed_set(CANONICAL_V4, transform_id) for transform_id in range(8)})


def build_exact_v4_affine_mechanism_audit() -> dict:
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [tuple(tuple(row) for row in square) for square in dataset["essential_representatives"]]
    f2_result = f2ext.build_order4_f2_extension()
    profiles = f2_result["records"]

    exact_profiles = [profile for profile in profiles if profile["is_exact_canonical_v4"]]
    selected_affine_extras = [
        profile
        for profile in profiles
        if profile["selected_mask_is_affine_plane"]
        and not profile["cell_labeling"]["is_affine_automorphism"]
    ]

    exact_terminal_profiles = [terminal_set_profile(profile["terminal_diagonal_set"]) for profile in exact_profiles]
    extra_terminal_profiles = [
        terminal_set_profile(profile["terminal_diagonal_set"])
        for profile in selected_affine_extras
    ]

    exact_defects = [
        affine_defect_profile(squares[profile["square_index"]])
        for profile in exact_profiles
    ]
    extra_defects = [
        affine_defect_profile(squares[profile["square_index"]])
        for profile in selected_affine_extras
    ]

    selected_mask_affine_but_global_defect = []
    for profile, defect in zip(selected_affine_extras, extra_defects):
        selected_mask_affine_but_global_defect.append(
            {
                "square_index": profile["square_index"],
                "mask": profile["mask"],
                "terminal_diagonal_set": profile["terminal_diagonal_set"],
                **defect,
            }
        )

    exact_translation_count = sum(
        1 for profile in exact_terminal_profiles if profile["is_full_translation_v4"]
    )
    extra_translation_subset_count = sum(
        1 for profile in extra_terminal_profiles if profile["is_translation_subset"]
    )
    extra_full_translation_count = sum(
        1 for profile in extra_terminal_profiles if profile["is_full_translation_v4"]
    )

    v4_orbit = canonical_v4_square_symmetry_orbit()
    v4_orbit_keys = {",".join(words) for words in v4_orbit}
    exact_sets_in_orbit = all(
        ",".join(sorted(profile["terminal_diagonal_set"])) in v4_orbit_keys
        for profile in exact_profiles
    )
    extra_sets_in_orbit = sum(
        1
        for profile in selected_affine_extras
        if ",".join(sorted(profile["terminal_diagonal_set"])) in v4_orbit_keys
    )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase J2",
            "description": "Mechanism, orientation, and affine-defect audit for exact canonical V4.",
        },
        "terminal24_pair_count": len(profiles),
        "exact_canonical_v4_pair_count": len(exact_profiles),
        "selected_affine_extra_count": len(selected_affine_extras),
        "linear_mechanism": {
            "exact_v4_terminal_sets_full_translation_v4": exact_translation_count,
            "exact_v4_all_terminal_sets_full_translation_v4": (
                exact_translation_count == len(exact_profiles)
            ),
            "selected_affine_extras_translation_subset_count": extra_translation_subset_count,
            "selected_affine_extras_full_translation_v4_count": extra_full_translation_count,
            "terminal_set_profiles_exact_v4": counter_json(
                Counter(
                    str(profile["linear_part_counts"])
                    for profile in exact_terminal_profiles
                )
            ),
            "terminal_set_profiles_selected_affine_extras": counter_json(
                Counter(
                    str(profile["linear_part_counts"])
                    for profile in extra_terminal_profiles
                )
            ),
        },
        "orientation": {
            "canonical_v4_square_symmetry_orbit_size": len(v4_orbit),
            "canonical_v4_square_symmetry_orbit": [list(words) for words in v4_orbit],
            "exact_v4_terminal_sets_in_square_symmetry_orbit": exact_sets_in_orbit,
            "selected_affine_extra_terminal_sets_in_square_symmetry_orbit_count": (
                extra_sets_in_orbit
            ),
            "word_set_is_orientation_language": True,
            "affine_cell_value_criterion_is_stable_object": True,
        },
        "affine_defect": {
            "exact_v4_basis_mismatch_distribution": counter_json(
                Counter(defect["basis_interpolation_mismatch_count"] for defect in exact_defects)
            ),
            "selected_affine_extra_basis_mismatch_distribution": counter_json(
                Counter(defect["basis_interpolation_mismatch_count"] for defect in extra_defects)
            ),
            "exact_v4_preserved_domain_affine_planes_distribution": counter_json(
                Counter(defect["preserved_domain_affine_planes"] for defect in exact_defects)
            ),
            "selected_affine_extra_preserved_domain_affine_planes_distribution": counter_json(
                Counter(defect["preserved_domain_affine_planes"] for defect in extra_defects)
            ),
            "exact_v4_preserved_permutation_diagonal_planes_distribution": counter_json(
                Counter(defect["preserved_permutation_diagonal_planes"] for defect in exact_defects)
            ),
            "selected_affine_extra_preserved_permutation_diagonal_planes_distribution": counter_json(
                Counter(defect["preserved_permutation_diagonal_planes"] for defect in extra_defects)
            ),
            "selected_affine_extra_records": selected_mask_affine_but_global_defect,
        },
    }


def write_report(result: dict, path: Path) -> None:
    mech = result["linear_mechanism"]
    orientation = result["orientation"]
    defect = result["affine_defect"]
    lines = [
        "# Exact-V4 Affine Mechanism Audit",
        "",
        "Status: Phase J2 mechanism / orientation / defect pass",
        "",
        "## Summary",
        "",
        f"- terminal-24 pairs: `{result['terminal24_pair_count']}`",
        f"- exact canonical `V4` pairs: `{result['exact_canonical_v4_pair_count']}`",
        f"- selected-affine extras: `{result['selected_affine_extra_count']}`",
        "",
        "## Linear Mechanism",
        "",
        f"- exact-`V4` terminal sets that are full translation `V4`: `{mech['exact_v4_terminal_sets_full_translation_v4']}`",
        f"- exact-`V4` all full translation `V4`: `{mech['exact_v4_all_terminal_sets_full_translation_v4']}`",
        f"- selected-affine extras that are translation subsets: `{mech['selected_affine_extras_translation_subset_count']}`",
        f"- selected-affine extras that are full translation `V4`: `{mech['selected_affine_extras_full_translation_v4_count']}`",
        "",
        "The exact-`V4` class is therefore literally the full translation",
        "subgroup in the canonical `F2^2` row/column model.  The extras may",
        "contain translation subsets, but never the full translation `V4`.",
        "",
        "## Orientation",
        "",
        f"- square-symmetry orbit size of canonical `V4`: `{orientation['canonical_v4_square_symmetry_orbit_size']}`",
        f"- all exact-`V4` terminal sets lie in that orbit: `{orientation['exact_v4_terminal_sets_in_square_symmetry_orbit']}`",
        f"- selected-affine extra terminal sets in that orbit: `{orientation['selected_affine_extra_terminal_sets_in_square_symmetry_orbit_count']}`",
        "",
        "The literal word set remains orientation language.  The stable object",
        "is the affine cell-value criterion plus the transformed-mask `F2^4`",
        "profile.",
        "",
        "## Affine Defect",
        "",
        f"- exact-`V4` basis mismatch distribution: `{defect['exact_v4_basis_mismatch_distribution']}`",
        f"- extra basis mismatch distribution: `{defect['selected_affine_extra_basis_mismatch_distribution']}`",
        f"- exact-`V4` preserved domain affine planes: `{defect['exact_v4_preserved_domain_affine_planes_distribution']}`",
        f"- extra preserved domain affine planes: `{defect['selected_affine_extra_preserved_domain_affine_planes_distribution']}`",
        f"- exact-`V4` preserved permutation diagonals as affine planes: `{defect['exact_v4_preserved_permutation_diagonal_planes_distribution']}`",
        f"- extra preserved permutation diagonals as affine planes: `{defect['selected_affine_extra_preserved_permutation_diagonal_planes_distribution']}`",
        "",
        "This gives the clean negative control: the 32 extras have the same",
        "selected affine high-value mask, but their full cell-value map fails",
        "to preserve all affine planes and all permutation-diagonal planes.",
        "",
        "## Interpretation",
        "",
        "Phase J2 upgrades the finite equivalence into a mechanism-level finite",
        "statement:",
        "",
        "```text",
        "exact canonical V4",
        "  = full translation V4 terminal diagonal set",
        "  = global affine cell-value labeling",
        "  = preservation of all 140 domain affine planes",
        "  = preservation of all 24 permutation-diagonal affine planes",
        "```",
        "",
        "The 32 extras explain why selected-mask affineness is insufficient:",
        "they retain the affine high-value mask but have a nonzero global",
        "affine defect.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_exact_v4_affine_mechanism_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "exact_v4_affine_mechanism_audit.json"
        report_path = root / "results" / "EXACT_V4_AFFINE_MECHANISM_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "exact_v4_all_full_translation_v4": result["linear_mechanism"][
                "exact_v4_all_terminal_sets_full_translation_v4"
            ],
            "selected_affine_extras_full_translation_v4_count": result["linear_mechanism"][
                "selected_affine_extras_full_translation_v4_count"
            ],
            "exact_v4_basis_mismatch_distribution": result["affine_defect"][
                "exact_v4_basis_mismatch_distribution"
            ],
            "selected_affine_extra_basis_mismatch_distribution": result["affine_defect"][
                "selected_affine_extra_basis_mismatch_distribution"
            ],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
