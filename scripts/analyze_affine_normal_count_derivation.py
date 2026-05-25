"""Phase O4 linear-algebra derivation of the 432 affine representatives."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import analyze_f2_orientation_stability as orientation
import enumerate_order4_endpoints as order4


BITS = (8, 4, 2, 1)


def gf2_rank(rows: list[int] | tuple[int, ...]) -> int:
    rows = list(rows)
    rank = 0
    for bit in BITS:
        pivot = next((i for i in range(rank, len(rows)) if rows[i] & bit), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] & bit:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def two_planes() -> list[tuple[int, int, int, int]]:
    planes = set()
    for values in itertools.combinations(range(1, 16), 3):
        plane = tuple(sorted((0, *values)))
        if gf2_rank(plane) != 2:
            continue
        if all((a ^ b) in plane for a in plane for b in plane):
            planes.add(plane)
    return sorted(planes)


def is_balanced_direction(plane: tuple[int, int, int, int]) -> bool:
    return all(
        any(value & bit for value in plane)
        and any(not (value & bit) for value in plane)
        for bit in BITS
    )


def span_rank(*planes: tuple[int, int, int, int]) -> int:
    rows = []
    for plane in planes:
        rows.extend(plane)
    return gf2_rank(rows)


def gl4_columns() -> list[tuple[int, int, int, int]]:
    return [
        tuple(columns)  # type: ignore[list-item]
        for columns in itertools.permutations(range(1, 16), 4)
        if gf2_rank(columns) == 4
    ]


def apply_linear(columns: tuple[int, int, int, int], value: int) -> int:
    out = 0
    for bit, column in zip(BITS, columns):
        if value & bit:
            out ^= column
    return out


def image_plane(
    columns: tuple[int, int, int, int],
    plane: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(sorted(apply_linear(columns, value) for value in plane))  # type: ignore[return-value]


def direction_sum_is_magic(plane: tuple[int, int, int, int]) -> bool:
    """All cosets of a balanced direction have label sum 30, hence value sum 34."""

    return is_balanced_direction(plane)


def build_affine_normal_count_derivation() -> dict:
    planes = two_planes()
    balanced = [plane for plane in planes if is_balanced_direction(plane)]
    balanced_set = set(balanced)

    # Domain directions for rows, columns, and the two main diagonals in the
    # row-bit/column-bit model.  The two diagonals are parallel affine planes,
    # so they share one direction.
    row_direction = (0, 1, 2, 3)
    column_direction = (0, 4, 8, 12)
    diagonal_direction = (0, 5, 10, 15)
    domain_magic_directions = (
        row_direction,
        column_direction,
        diagonal_direction,
    )

    ordered_balanced_triples = [
        (first, second, third)
        for first in balanced
        for second in balanced
        for third in balanced
        if span_rank(first, second) == 4
        and span_rank(first, third) == 4
        and span_rank(second, third) == 4
    ]

    complementarity_edges = [
        (first, second)
        for index, first in enumerate(balanced)
        for second in balanced[index + 1 :]
        if span_rank(first, second) == 4
    ]
    complementarity_edge_set = {
        (first, second) for first, second in complementarity_edges
    }
    complementarity_triangles = [
        (first, second, third)
        for first, second, third in itertools.combinations(balanced, 3)
        if (min(first, second), max(first, second)) in complementarity_edge_set
        and (min(first, third), max(first, third)) in complementarity_edge_set
        and (min(second, third), max(second, third)) in complementarity_edge_set
    ]

    good_linear_parts = []
    image_triple_counter = Counter()
    stabilizer_count = 0
    for columns in gl4_columns():
        image_triple = tuple(
            image_plane(columns, direction)
            for direction in domain_magic_directions
        )
        if all(image in balanced_set for image in image_triple):
            good_linear_parts.append(columns)
            image_triple_counter[image_triple] += 1
        if image_triple == domain_magic_directions:
            stabilizer_count += 1

    offset_count = 16
    raw_affine_magic_square_count = len(good_linear_parts) * offset_count
    square_symmetry_orbit_size = 8
    essential_affine_representative_count = (
        raw_affine_magic_square_count // square_symmetry_orbit_size
    )

    admissible_masks = [
        order4.perm_string(mask) for mask in order4.admissible_one_incidence_perms()
    ]
    mask_orbits = {
        mask: tuple(
            sorted(orientation.transform_mask(mask, transform_id) for transform_id in range(8))
        )
        for mask in admissible_masks
    }
    mask_stabilizers = {
        mask: tuple(
            transform_id
            for transform_id in range(8)
            if orientation.transform_mask(mask, transform_id) == mask
        )
        for mask in admissible_masks
    }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O4",
            "description": "Linear-algebra count derivation for the 432 globally affine essential representatives.",
        },
        "two_dimensional_subspace_count": len(planes),
        "balanced_direction_count": len(balanced),
        "balanced_directions": [list(plane) for plane in balanced],
        "domain_magic_directions": {
            "row": list(row_direction),
            "column": list(column_direction),
            "diagonal_and_antidiagonal": list(diagonal_direction),
        },
        "domain_magic_directions_pairwise_complementary": all(
            span_rank(a, b) == 4
            for a, b in itertools.combinations(domain_magic_directions, 2)
        ),
        "ordered_pairwise_complementary_balanced_triple_count": len(
            ordered_balanced_triples
        ),
        "balanced_complementarity_graph": {
            "vertex_count": len(balanced),
            "edge_count": len(complementarity_edges),
            "triangle_count": len(complementarity_triangles),
            "ordered_triangle_count": 6 * len(complementarity_triangles),
        },
        "gl4_linear_part_count": len(gl4_columns()),
        "good_linear_part_count": len(good_linear_parts),
        "image_triple_count": len(image_triple_counter),
        "image_triple_multiplicity_distribution": {
            str(key): value
            for key, value in sorted(Counter(image_triple_counter.values()).items())
        },
        "domain_triple_stabilizer_size": stabilizer_count,
        "offset_count": offset_count,
        "raw_affine_magic_square_count": raw_affine_magic_square_count,
        "square_symmetry_orbit_size_for_normal_squares": square_symmetry_orbit_size,
        "essential_affine_representative_count": essential_affine_representative_count,
        "admissible_mask_torsor": {
            "admissible_mask_count": len(admissible_masks),
            "square_symmetry_count": 8,
            "orbit_count": len(set(mask_orbits.values())),
            "orbit_size_distribution": {
                str(key): value
                for key, value in sorted(
                    Counter(len(orbit) for orbit in mask_orbits.values()).items()
                )
            },
            "stabilizer_size_distribution": {
                str(key): value
                for key, value in sorted(
                    Counter(len(stabilizer) for stabilizer in mask_stabilizers.values()).items()
                )
            },
            "is_free_transitive": (
                len(set(mask_orbits.values())) == 1
                and set(len(orbit) for orbit in mask_orbits.values()) == {8}
                and set(len(stabilizer) for stabilizer in mask_stabilizers.values()) == {1}
            ),
        },
        "derivation": {
            "good_linear_parts": "36 balanced triples x 6 maps per triple = 216",
            "raw_affine_magic_squares": "216 linear parts x 16 offsets = 3456",
            "essential_affine_representatives": "3456 raw squares / 8 square symmetries = 432",
        },
        "guardrail": (
            "This is a finite F2-linear count, not a classification theorem for "
            "non-affine order-4 magic squares or for higher orders."
        ),
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Affine Normal Count Derivation",
        "",
        "Status: Phase O4 linear-algebra derivation",
        "",
        "## Purpose",
        "",
        "Phase O2/O3 reduced the `144` exact-V4 story to the globally affine",
        "normal order-4 layer.  This audit derives the total `432` count without",
        "enumerating the `880` essential representatives.",
        "",
        "## Linear-Algebra Count",
        "",
        f"- 2-dimensional subspaces of `F2^4`: `{result['two_dimensional_subspace_count']}`",
        f"- balanced directions: `{result['balanced_direction_count']}`",
        f"- ordered pairwise-complementary balanced triples: `{result['ordered_pairwise_complementary_balanced_triple_count']}`",
        f"- maps per image triple: `{result['domain_triple_stabilizer_size']}`",
        f"- good linear parts: `{result['good_linear_part_count']}`",
        f"- complementarity graph triangles: `{result['balanced_complementarity_graph']['triangle_count']}`",
        "",
        "The three relevant domain directions are row, column, and diagonal",
        "direction.  The main and anti-diagonal are parallel affine planes, so",
        "they share the same direction.",
        "",
        "A linear part is good exactly when those three directions map to balanced",
        "directions in value space.  The count is:",
        "",
        "```text",
        "36 balanced image triples x 6 maps per triple = 216 linear parts",
        "```",
        "",
        "Equivalently, the complementarity graph on the 13 balanced directions",
        "has 6 triangles, and each triangle has 6 orderings.",
        "",
        "## From Linear Parts To Essential Representatives",
        "",
        "Offsets are free: adding an affine offset in value space translates all",
        "labels and preserves the balanced-direction line sums.",
        "",
        "```text",
        "216 linear parts x 16 offsets = 3456 raw affine normal squares",
        "3456 / 8 square symmetries = 432 essential representatives",
        "```",
        "",
        "The division by `8` is valid for normal squares because all entries are",
        "distinct, so no nontrivial square symmetry can fix a square cellwise.",
        "The same square-symmetry group acts freely and transitively on the",
        "eight admissible one-incidence masks:",
        "",
        "```text",
        f"{result['admissible_mask_torsor']}",
        "```",
        "",
        "## Link To The 144 Class",
        "",
        "Combining this with Phase O3 gives:",
        "",
        "```text",
        "432 globally affine essential representatives",
        "  = 3 coordinate-axis matchings x 144",
        "",
        "432 x 8 admissible masks",
        "  = 3456 affine square-mask pairs",
        "  = 24 selected value planes x 144",
        "```",
        "",
        "The terminal-24 exact-V4 class is the high value plane",
        "`{11,12,15,16}`.",
        "",
        "## Guardrail",
        "",
        result["guardrail"],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_affine_normal_count_derivation()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "affine_normal_count_derivation.json"
        report_path = root / "results" / "AFFINE_NORMAL_COUNT_DERIVATION_REPORT.md"
        json_path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        write_report(result, report_path)
        print(f"wrote {json_path}")
        print(f"wrote {report_path}")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
