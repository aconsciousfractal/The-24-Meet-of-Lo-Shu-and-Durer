"""F2^4 / tesseract layer for the Magic 24 project.

Sudbery's Durer-tesseract viewpoint labels each Durer cell by its value
minus one, hence by a point of the affine space F2^4.  A four-cell set is an
affine plane in this model exactly when the xor of its four labels is zero.

This script tests the external-agent proposal that the Sagrada ray has a
real F2^4 layer:

- the eight one-incidence masks are affine planes;
- the Sagrada mask is the unique one whose Durer terminal is 24;
- the 86 Durer quaternes split into affine and non-affine pieces;
- the terminal H_24(D(10)) hypergraph has a clean affine/non-affine split;
- the diagonal break D4 -> V4 is a break from two affine-map families to the
  translation subgroup on F2^2.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

import magic24_certificates as magic24


Cell = tuple[int, int]
Quad = tuple[Cell, Cell, Cell, Cell]
Perm = tuple[int, int, int, int]


def perm_from_string(text: str) -> Perm:
    return tuple(int(c) for c in text)  # type: ignore[return-value]


def perm_string(p: Perm) -> str:
    return "".join(str(x) for x in p)


def encode_cells(cells: Iterable[Cell]) -> list[str]:
    return [f"{i},{j}" for i, j in cells]


def cell_label(cell: Cell) -> int:
    """Return the F2^4 label, encoded as an integer in [0, 15]."""

    i, j = cell
    return magic24.d_value(i, j) - 1


def label_bits(label: int) -> str:
    return format(label, "04b")


def label_bit_vector(label: int) -> tuple[int, int, int, int]:
    """Return the bits of a label in the documented MSB-to-LSB order."""

    return tuple((label >> shift) & 1 for shift in (3, 2, 1, 0))  # type: ignore[return-value]


def bits_to_label(bits: Iterable[int]) -> int:
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out


def cell_input_bits(cell: Cell) -> tuple[int, int, int, int]:
    """Encode (row, column) as high/low row bits and high/low column bits."""

    i, j = cell
    return ((i >> 1) & 1, i & 1, (j >> 1) & 1, j & 1)


LINEAR_LABEL_MATRIX_ROWS = (
    (0, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 1, 0),
    (1, 1, 0, 1),
)


LINEAR_LABEL_FORMULAS = (
    "l0 = r1 + c0 + c1",
    "l1 = r0 + c0 + c1",
    "l2 = r0 + r1 + c0",
    "l3 = r0 + r1 + c1",
)


def linear_label_bits_from_cell_bits(
    bits: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(sum(a * b for a, b in zip(row, bits)) % 2 for row in LINEAR_LABEL_MATRIX_ROWS)  # type: ignore[return-value]


def gf2_rank(rows: Iterable[Iterable[int]]) -> int:
    """Rank over F2 for short binary rows."""

    encoded = []
    for row in rows:
        value = 0
        for bit in row:
            value = (value << 1) | (bit & 1)
        encoded.append(value)

    rank = 0
    bit = 1 << 3
    while bit:
        pivot = next((i for i in range(rank, len(encoded)) if encoded[i] & bit), None)
        if pivot is not None:
            encoded[rank], encoded[pivot] = encoded[pivot], encoded[rank]
            for i in range(len(encoded)):
                if i != rank and encoded[i] & bit:
                    encoded[i] ^= encoded[rank]
            rank += 1
        bit >>= 1
    return rank


def cell_record(cell: Cell) -> dict:
    i, j = cell
    label = cell_label(cell)
    return {
        "cell": f"{i},{j}",
        "value": magic24.d_value(i, j),
        "label": label,
        "bits": label_bits(label),
    }


def quad_xor(quad: Iterable[Cell]) -> int:
    out = 0
    for cell in quad:
        out ^= cell_label(cell)
    return out


def is_affine_plane(quad: Iterable[Cell]) -> bool:
    cells = tuple(quad)
    return len(cells) == 4 and len(set(cells)) == 4 and quad_xor(cells) == 0


def all_quads() -> list[Quad]:
    return list(itertools.combinations(magic24.all_cells(), 4))  # type: ignore[return-value]


def all_affine_planes() -> list[Quad]:
    return [quad for quad in all_quads() if is_affine_plane(quad)]


def label_set(quad: Iterable[Cell]) -> tuple[int, int, int, int]:
    return tuple(sorted(cell_label(cell) for cell in quad))  # type: ignore[return-value]


def source_sum(quad: Iterable[Cell]) -> int:
    return sum(magic24.d_value(i, j) for i, j in quad)


def terminal_sum(quad: Iterable[Cell], t: int = 10) -> int:
    return sum(magic24.durer_t_value(i, j, t) for i, j in quad)


def mask_cells(mask: Perm) -> Quad:
    return tuple((i, mask[i]) for i in range(4))  # type: ignore[return-value]


def all_permutation_diagonal_quads() -> list[Quad]:
    return [mask_cells(tuple(p)) for p in itertools.permutations(range(4))]  # type: ignore[list-item]


def all_two_dimensional_directions() -> list[tuple[int, int, int, int]]:
    directions = set()
    for a, b in itertools.combinations(range(1, 16), 2):
        directions.add(tuple(sorted((0, a, b, a ^ b))))
    return sorted(directions)


def cosets_of_direction(direction: Iterable[int]) -> list[tuple[int, int, int, int]]:
    direction_set = set(direction)
    cosets = {
        tuple(sorted(rep ^ v for v in direction_set))
        for rep in range(16)
    }
    return sorted(cosets)


def is_balanced_direction(direction: Iterable[int]) -> bool:
    """A direction is balanced when no coordinate bit is constant on its cosets."""

    direction_set = tuple(direction)
    return all(any((v >> bit) & 1 for v in direction_set) for bit in range(4))


def plane_direction(labels: Iterable[int]) -> tuple[int, int, int, int]:
    labels_tuple = tuple(labels)
    base = labels_tuple[0]
    return tuple(sorted(base ^ label for label in labels_tuple))  # type: ignore[return-value]


def subspace_intersection_dimension(
    left: Iterable[int], right: Iterable[int]
) -> int:
    size = len(set(left) & set(right))
    if size == 1:
        return 0
    if size == 2:
        return 1
    if size == 4:
        return 2
    raise ValueError(f"unexpected F2 subspace intersection size: {size}")


def build_linear_coordination_layer() -> dict:
    records = []
    for cell in magic24.all_cells():
        input_bits = cell_input_bits(cell)
        formula_bits = linear_label_bits_from_cell_bits(input_bits)
        actual_label = cell_label(cell)
        records.append(
            {
                "cell": f"{cell[0]},{cell[1]}",
                "input_bits_r0_r1_c0_c1": list(input_bits),
                "actual_label": actual_label,
                "actual_bits_l0_l1_l2_l3": list(label_bit_vector(actual_label)),
                "formula_bits_l0_l1_l2_l3": list(formula_bits),
                "formula_label": bits_to_label(formula_bits),
                "matches": label_bit_vector(actual_label) == formula_bits,
            }
        )

    permutation_diagonal_quads = all_permutation_diagonal_quads()
    return {
        "input_bit_order": ["r0=row_high", "r1=row_low", "c0=column_high", "c1=column_low"],
        "output_bit_order": ["l0=label_bit_8", "l1=label_bit_4", "l2=label_bit_2", "l3=label_bit_1"],
        "formulas_over_f2": list(LINEAR_LABEL_FORMULAS),
        "matrix_rows": [list(row) for row in LINEAR_LABEL_MATRIX_ROWS],
        "matrix_rank_over_f2": gf2_rank(LINEAR_LABEL_MATRIX_ROWS),
        "is_linear_automorphism": gf2_rank(LINEAR_LABEL_MATRIX_ROWS) == 4,
        "all_cells_match_formula": all(record["matches"] for record in records),
        "cell_records": records,
        "all_24_permutation_diagonals_are_affine_planes": all(
            is_affine_plane(quad) for quad in permutation_diagonal_quads
        ),
    }


def build_mask_layer() -> dict:
    rows = []
    for row in magic24.durer_one_incidence_masks()["masks"]:
        mask = perm_from_string(row["perm"])
        cells = mask_cells(mask)
        labels = [cell_label(cell) for cell in cells]
        rows.append(
            {
                **row,
                "cells": encode_cells(cells),
                "labels": labels,
                "bits": [label_bits(label) for label in labels],
                "label_xor": quad_xor(cells),
                "is_affine_plane": is_affine_plane(cells),
            }
        )

    return {
        "one_incidence_count": len(rows),
        "all_one_incidence_masks_are_affine_planes": all(
            row["is_affine_plane"] for row in rows
        ),
        "terminal_24_affine_plane_masks": [
            row["perm"]
            for row in rows
            if row["terminal_sum"] == 24 and row["is_affine_plane"]
        ],
        "sagrada_mask": {
            "perm": "2013",
            "cells": encode_cells(mask_cells(magic24.SAGRADA_MASK_PERM)),
            "cell_records": [cell_record(cell) for cell in mask_cells(magic24.SAGRADA_MASK_PERM)],
        },
        "masks": rows,
    }


def counter_to_sorted_dict(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter)}


def nested_counter_to_dict(counter: Counter) -> dict[str, int]:
    return {
        "_".join(str(x) for x in key): value
        for key, value in sorted(counter.items())
    }


def build_affine_direction_layer() -> dict:
    directions = all_two_dimensional_directions()
    all_direction_cosets = {
        coset
        for direction in directions
        for coset in cosets_of_direction(direction)
    }
    ambient_affine_label_sets = {label_set(quad) for quad in all_affine_planes()}
    balanced_directions = [direction for direction in directions if is_balanced_direction(direction)]
    balanced_cosets = {
        coset
        for direction in balanced_directions
        for coset in cosets_of_direction(direction)
    }
    h34_affine_label_sets = {
        label_set(quad)
        for quad in all_quads()
        if source_sum(quad) == 34 and is_affine_plane(quad)
    }

    sagrada_labels = label_set(mask_cells(magic24.SAGRADA_MASK_PERM))
    sagrada_direction = plane_direction(sagrada_labels)

    relation_counts = Counter()
    incidence_counts = Counter()
    complementary_transport_cosets = set()
    line_intersection_cosets = set()
    for direction in balanced_directions:
        intersection_dimension = subspace_intersection_dimension(direction, sagrada_direction)
        if intersection_dimension == 0:
            relation = "complementary_to_sagrada_direction"
        elif intersection_dimension == 1:
            relation = "line_intersection_with_sagrada_direction"
        else:
            relation = "same_as_sagrada_direction"
        relation_counts[relation] += 1

        for coset in cosets_of_direction(direction):
            incidence = len(set(coset) & set(sagrada_labels))
            incidence_counts[(relation, incidence)] += 1
            if relation == "complementary_to_sagrada_direction":
                complementary_transport_cosets.add(coset)
            elif relation == "line_intersection_with_sagrada_direction":
                line_intersection_cosets.add(coset)

    terminal_affine_label_sets = {
        label_set(quad)
        for quad in all_quads()
        if terminal_sum(quad, 10) == 24 and is_affine_plane(quad)
    }

    return {
        "two_dimensional_direction_count": len(directions),
        "affine_plane_count_from_direction_cosets": len(all_direction_cosets),
        "direction_cosets_equal_ambient_affine_planes": all_direction_cosets == ambient_affine_label_sets,
        "balanced_direction_count": len(balanced_directions),
        "balanced_coset_count": len(balanced_cosets),
        "balanced_cosets_equal_h34_affine_planes": balanced_cosets == h34_affine_label_sets,
        "sagrada_label_plane": list(sagrada_labels),
        "sagrada_direction": list(sagrada_direction),
        "sagrada_direction_is_balanced": is_balanced_direction(sagrada_direction),
        "balanced_direction_relation_to_sagrada": dict(sorted(relation_counts.items())),
        "balanced_coset_incidence_by_relation": nested_counter_to_dict(incidence_counts),
        "complementary_balanced_coset_count": len(complementary_transport_cosets),
        "line_intersection_balanced_coset_count": len(line_intersection_cosets),
        "terminal_affine_planes_equal_complementary_balanced_cosets": (
            terminal_affine_label_sets == complementary_transport_cosets
        ),
    }


def build_quaterne_layer() -> dict:
    quads = all_quads()
    affine_planes = all_affine_planes()
    h34 = [quad for quad in quads if source_sum(quad) == 34]
    h24_terminal = [quad for quad in quads if terminal_sum(quad, 10) == 24]

    h34_affine_counter = Counter(
        "affine" if is_affine_plane(quad) else "non_affine" for quad in h34
    )
    h34_by_incidence_and_affine = Counter(
        (
            magic24.mask_incidence(quad),
            "affine" if is_affine_plane(quad) else "non_affine",
        )
        for quad in h34
    )
    h24_affine_counter = Counter(
        "affine" if is_affine_plane(quad) else "non_affine" for quad in h24_terminal
    )
    h24_by_source_incidence_affine = Counter(
        (
            source_sum(quad),
            magic24.mask_incidence(quad),
            "affine" if is_affine_plane(quad) else "non_affine",
        )
        for quad in h24_terminal
    )

    terminal_affine_from_transport = [
        quad
        for quad in h24_terminal
        if is_affine_plane(quad)
        and source_sum(quad) == 34
        and magic24.mask_incidence(quad) == 1
    ]

    return {
        "ambient_four_cell_sets": len(quads),
        "ambient_affine_planes": len(affine_planes),
        "ambient_affine_plane_source_sum_distribution": counter_to_sorted_dict(
            Counter(source_sum(quad) for quad in affine_planes)
        ),
        "h34_count": len(h34),
        "h34_affine_split": dict(sorted(h34_affine_counter.items())),
        "h34_by_sagrada_incidence_and_affine_split": nested_counter_to_dict(
            h34_by_incidence_and_affine
        ),
        "transported_h34_incidence1_affine_split": {
            key: h34_by_incidence_and_affine[(1, key)]
            for key in ("affine", "non_affine")
        },
        "d10_h24_count": len(h24_terminal),
        "d10_h24_affine_split": dict(sorted(h24_affine_counter.items())),
        "d10_h24_by_source_incidence_affine_split": nested_counter_to_dict(
            h24_by_source_incidence_affine
        ),
        "d10_h24_affine_planes_are_exactly_transported_h34_incidence1": (
            len(terminal_affine_from_transport) == h24_affine_counter["affine"]
        ),
    }


def bit_swap(x: int) -> int:
    return ((x & 1) << 1) | ((x & 2) >> 1)


def is_translation(p: Perm) -> bool:
    b = p[0]
    return all(p[x] == (x ^ b) for x in range(4))


def is_bit_swap_translate(p: Perm) -> bool:
    b = p[0]
    return all(p[x] == (bit_swap(x) ^ b) for x in range(4))


def affine_family_name(p: Perm) -> str:
    if is_translation(p):
        return "identity_linear_part_translation"
    if is_bit_swap_translate(p):
        return "bit_swap_linear_part_translation"
    return "other"


def build_diagonal_affine_layer() -> dict:
    diagonals = magic24.durer_permutation_diagonals()["target_diagonals_by_t"]
    d4 = [perm_from_string(word) for word in diagonals["0"]]
    v4 = [perm_from_string(word) for word in diagonals["1"]]

    def rows(perms: Iterable[Perm]) -> list[dict]:
        out = []
        for p in sorted(perms):
            out.append(
                {
                    "perm": perm_string(p),
                    "family": affine_family_name(p),
                    "translation_parameter": p[0],
                }
            )
        return out

    return {
        "source_D4": {
            "perms": rows(d4),
            "family_counts": dict(sorted(Counter(affine_family_name(p) for p in d4).items())),
            "is_union_of_translation_and_bit_swap_translation_families": all(
                affine_family_name(p) != "other" for p in d4
            ),
        },
        "terminal_V4": {
            "perms": rows(v4),
            "family_counts": dict(sorted(Counter(affine_family_name(p) for p in v4).items())),
            "is_translation_subgroup": all(is_translation(p) for p in v4),
        },
    }


def build_f2_tesseract_analysis() -> dict:
    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase F",
            "description": "F2^4 / Durer-tesseract classification of one-incidence masks, quaternes, and D4 -> V4 diagonal break.",
            "cell_model": "The Durer value v in a cell is relabeled by v-1 in {0,...,15}=F2^4.",
            "affine_plane_test": "A four-cell set is an affine plane iff the xor of the four labels is zero.",
        },
        "linear_coordination_layer": build_linear_coordination_layer(),
        "mask_layer": build_mask_layer(),
        "affine_direction_layer": build_affine_direction_layer(),
        "quaterne_layer": build_quaterne_layer(),
        "diagonal_affine_layer": build_diagonal_affine_layer(),
    }


def write_report(result: dict, path: Path) -> None:
    q = result["quaterne_layer"]
    m = result["mask_layer"]
    l = result["linear_coordination_layer"]
    a = result["affine_direction_layer"]
    d = result["diagonal_affine_layer"]
    lines = [
        "# F2^4 Tesseract Report",
        "",
        "Status: Phase F exact finite replay plus structural finite-affine lemmas",
        "",
        "## Model",
        "",
        "Each Durer cell is labeled by `value-1`, hence by a point of `F2^4`.",
        "A four-cell set is treated as an affine plane exactly when the xor of",
        "its four labels is zero.",
        "",
        "## Linear Tesseract Coordinatization",
        "",
        "With row and column written in high/low bits `(r0,r1)` and `(c0,c1)`,",
        "and with `D[r,c]-1` written MSB-to-LSB as `(l0,l1,l2,l3)`, the value",
        "labeling is the following linear map over `F2`:",
        "",
        "```text",
        *l["formulas_over_f2"],
        "```",
        "",
        f"- matrix rank over `F2`: `{l['matrix_rank_over_f2']}`",
        f"- linear automorphism: `{l['is_linear_automorphism']}`",
        f"- all cells match formula: `{l['all_cells_match_formula']}`",
        f"- all 24 permutation diagonals are affine planes: `{l['all_24_permutation_diagonals_are_affine_planes']}`",
        "",
        "## One-Incidence Masks",
        "",
        f"- one-incidence masks: `{m['one_incidence_count']}`",
        f"- all one-incidence masks affine: `{m['all_one_incidence_masks_are_affine_planes']}`",
        f"- terminal-24 affine masks: `{m['terminal_24_affine_plane_masks']}`",
        "",
        "The affine-plane property does not by itself single out Sagrada.  All",
        "eight one-incidence masks have it; Sagrada is singled out only after",
        "adding the Durer bounded terminal condition.",
        "",
        "## Quaternes",
        "",
        f"- ambient four-cell sets: `{q['ambient_four_cell_sets']}`",
        f"- affine planes in the ambient `F2^4` cell model: `{q['ambient_affine_planes']}`",
        f"- `H_34(D)` count: `{q['h34_count']}`",
        f"- `H_34(D)` affine split: `{q['h34_affine_split']}`",
        f"- transported `H_34` incidence-1 affine split: `{q['transported_h34_incidence1_affine_split']}`",
        f"- `H_24(D(10))` count: `{q['d10_h24_count']}`",
        f"- `H_24(D(10))` affine split: `{q['d10_h24_affine_split']}`",
        f"- terminal affine planes are exactly transported source-34 incidence-1 planes: `{q['d10_h24_affine_planes_are_exactly_transported_h34_incidence1']}`",
        "",
        "## Balanced Directions",
        "",
        f"- 2-dimensional directions in `F2^4`: `{a['two_dimensional_direction_count']}`",
        f"- direction cosets / affine planes: `{a['affine_plane_count_from_direction_cosets']}`",
        f"- direction cosets equal ambient affine planes: `{a['direction_cosets_equal_ambient_affine_planes']}`",
        f"- balanced directions: `{a['balanced_direction_count']}`",
        f"- balanced direction cosets: `{a['balanced_coset_count']}`",
        f"- balanced cosets equal affine part of `H_34(D)`: `{a['balanced_cosets_equal_h34_affine_planes']}`",
        f"- relation of balanced directions to Sagrada direction: `{a['balanced_direction_relation_to_sagrada']}`",
        f"- incidence of balanced cosets by relation: `{a['balanced_coset_incidence_by_relation']}`",
        f"- terminal affine planes equal complementary balanced cosets: `{a['terminal_affine_planes_equal_complementary_balanced_cosets']}`",
        "",
        "Thus the source affine count is not an opaque replay: it is",
        "`13` balanced directions times `4` cosets.  The terminal affine count",
        "is the `9` balanced directions complementary to the Sagrada direction,",
        "again times `4` cosets.",
        "",
        "## Diagonal Groups",
        "",
        f"- source `D4` affine-family counts: `{d['source_D4']['family_counts']}`",
        f"- terminal `V4` affine-family counts: `{d['terminal_V4']['family_counts']}`",
        f"- terminal `V4` is the translation subgroup of `F2^2`: `{d['terminal_V4']['is_translation_subgroup']}`",
        "",
        "## Guardrail",
        "",
        "This layer strengthens the structure of the Durer/Sagrada cell, but it",
        "does not make `24` universal.  It also does not turn `D4` or `V4` into",
        "standard Type-A poset cones.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write F2^4 JSON and report")
    args = parser.parse_args()

    result = build_f2_tesseract_analysis()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "f2_tesseract_analysis.json"
        report_path = root / "results" / "F2_TESSERACT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "mask_layer": {
                "all_one_incidence_masks_are_affine_planes": result["mask_layer"][
                    "all_one_incidence_masks_are_affine_planes"
                ],
                "terminal_24_affine_plane_masks": result["mask_layer"][
                    "terminal_24_affine_plane_masks"
                ],
            },
            "quaterne_layer": {
                "h34_affine_split": result["quaterne_layer"]["h34_affine_split"],
                "d10_h24_affine_split": result["quaterne_layer"]["d10_h24_affine_split"],
                "terminal_affine_purity": result["quaterne_layer"][
                    "d10_h24_affine_planes_are_exactly_transported_h34_incidence1"
                ],
            },
            "affine_direction_layer": {
                "balanced_direction_count": result["affine_direction_layer"][
                    "balanced_direction_count"
                ],
                "balanced_cosets_equal_h34_affine_planes": result["affine_direction_layer"][
                    "balanced_cosets_equal_h34_affine_planes"
                ],
                "terminal_affine_purity": result["affine_direction_layer"][
                    "terminal_affine_planes_equal_complementary_balanced_cosets"
                ],
            },
            "diagonal_affine_layer": {
                "D4": result["diagonal_affine_layer"]["source_D4"]["family_counts"],
                "V4": result["diagonal_affine_layer"]["terminal_V4"]["family_counts"],
            },
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
