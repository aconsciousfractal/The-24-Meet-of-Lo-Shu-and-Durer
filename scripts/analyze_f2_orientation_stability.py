"""Micro-audit for orientation stability of the Phase-F F2^4 fingerprints."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import analyze_order4_f2_extension as f2
import enumerate_order4_endpoints as order4


Cell = tuple[int, int]
Square = tuple[tuple[int, ...], ...]


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def cell_to_input_index(cell: Cell) -> int:
    i, j = cell
    return (((i >> 1) & 1) << 3) | ((i & 1) << 2) | (((j >> 1) & 1) << 1) | (j & 1)


def input_index_to_cell(index: int) -> Cell:
    r0 = (index >> 3) & 1
    r1 = (index >> 2) & 1
    c0 = (index >> 1) & 1
    c1 = index & 1
    return ((r0 << 1) | r1, (c0 << 1) | c1)


def old_cell_for_transform(new_cell: Cell, transform_id: int) -> Cell:
    i, j = new_cell
    if transform_id == 0:
        return (i, j)
    if transform_id == 1:
        return (3 - j, i)
    if transform_id == 2:
        return (3 - i, 3 - j)
    if transform_id == 3:
        return (j, 3 - i)
    if transform_id == 4:
        return (3 - i, j)
    if transform_id == 5:
        return (i, 3 - j)
    if transform_id == 6:
        return (j, i)
    if transform_id == 7:
        return (3 - j, 3 - i)
    raise ValueError(f"bad transform id {transform_id}")


def transform_input_map(transform_id: int) -> tuple[int, ...]:
    return tuple(
        cell_to_input_index(old_cell_for_transform(input_index_to_cell(index), transform_id))
        for index in range(16)
    )


def affine_map_profile(mapping: tuple[int, ...]) -> dict:
    offset = mapping[0]
    columns = [mapping[index] ^ offset for index in (8, 4, 2, 1)]
    matches = True
    for index, actual in enumerate(mapping):
        predicted = offset
        for bit, column in zip((8, 4, 2, 1), columns):
            if index & bit:
                predicted ^= column
        if predicted != actual:
            matches = False
            break
    rank = f2.gf2_rank_int(columns)
    return {
        "is_affine": matches,
        "linear_rank_over_f2": rank,
        "is_affine_automorphism": matches and rank == 4,
        "offset": offset,
        "columns": columns,
    }


def square_profile(square: Square) -> dict:
    return f2.cell_labeling_affine_profile([list(row) for row in square])


def complement_square(square: Square) -> Square:
    return tuple(tuple(17 - value for value in row) for row in square)


def mask_cells(mask: str) -> tuple[Cell, Cell, Cell, Cell]:
    return tuple((i, int(mask[i])) for i in range(4))  # type: ignore[return-value]


def transform_mask(mask: str, transform_id: int) -> str:
    old_cells = set(mask_cells(mask))
    new_cells = [
        new_cell
        for new_cell in ((i, j) for i in range(4) for j in range(4))
        if old_cell_for_transform(new_cell, transform_id) in old_cells
    ]
    by_row = {i: j for i, j in new_cells}
    if sorted(by_row) != [0, 1, 2, 3] or len(set(by_row.values())) != 4:
        raise ValueError(f"transformed mask is not a permutation mask: {mask}, {transform_id}")
    return "".join(str(by_row[i]) for i in range(4))


def selected_values(square: Square, mask: str) -> list[int]:
    return [square[i][int(mask[i])] for i in range(4)]


def selected_f2_profile(square: Square, mask: str) -> dict:
    labels = [value - 1 for value in selected_values(square, mask)]
    direction = f2.plane_direction(labels)
    terminal = f2.label_space_terminal_profile(labels, t=min(labels))
    return {
        "sorted_values": sorted(value + 1 for value in labels),
        "selected_mask_is_affine_plane": direction is not None,
        "selected_mask_direction": list(direction) if direction else None,
        "terminal_affine_count": terminal["terminal_affine_count"],
        "terminal_affine_is_pure_transport": terminal["terminal_affine_is_pure_transport"],
        "transported_source34_incidence1_affine_count": terminal[
            "transported_source34_incidence1_affine_count"
        ],
    }


def build_orientation_stability_audit() -> dict:
    squares = order4.essential_order4_representatives()
    terminal24 = f2.load_json(
        Path(__file__).resolve().parents[1]
        / "results"
        / "order4_terminal24_fingerprints.json"
    )
    terminal_records = terminal24["records"]  # type: ignore[index]

    d4_domain_profiles = [
        {
            "transform_id": transform_id,
            "mapping": list(transform_input_map(transform_id)),
            **affine_map_profile(transform_input_map(transform_id)),
        }
        for transform_id in range(8)
    ]

    orientation_affine_counts = Counter()
    unstable_square_indices = []
    for index, square in enumerate(squares):
        flags = [
            square_profile(order4.transform_square(square, transform_id))[
                "is_affine_automorphism"
            ]
            for transform_id in range(8)
        ]
        orientation_affine_counts[sum(1 for flag in flags if flag)] += 1
        if len(set(flags)) != 1:
            unstable_square_indices.append(index)

    direct_complement_stable = []
    canonical_complement_stable = []
    for index, square in enumerate(squares):
        flag = square_profile(square)["is_affine_automorphism"]
        direct_complement_flag = square_profile(complement_square(square))[
            "is_affine_automorphism"
        ]
        canonical_complement_flag = square_profile(
            order4.canonical_square(complement_square(square))
        )["is_affine_automorphism"]
        if flag == direct_complement_flag:
            direct_complement_stable.append(index)
        if flag == canonical_complement_flag:
            canonical_complement_stable.append(index)

    unstable_terminal_records = []
    for record in terminal_records:
        square = squares[record["square_index"]]
        base = selected_f2_profile(square, record["mask"])
        for transform_id in range(8):
            transformed_square = order4.transform_square(square, transform_id)
            transformed_mask = transform_mask(record["mask"], transform_id)
            transformed = selected_f2_profile(transformed_square, transformed_mask)
            if transformed != base:
                unstable_terminal_records.append(
                    {
                        "square_index": record["square_index"],
                        "mask": record["mask"],
                        "transform_id": transform_id,
                        "transformed_mask": transformed_mask,
                        "base": base,
                        "transformed": transformed,
                    }
                )

    raw_affine_oriented_count = sum(
        orientation_count * square_count
        for orientation_count, square_count in orientation_affine_counts.items()
    )
    raw_total = 8 * len(squares)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase F orientation-stability micro-audit",
            "description": "Tests orientation and complement stability of the affine cell-value criterion and terminal-24 F2 profiles.",
        },
        "d4_domain_transform_profiles": d4_domain_profiles,
        "all_d4_domain_transforms_are_affine_automorphisms": all(
            profile["is_affine_automorphism"] for profile in d4_domain_profiles
        ),
        "essential_square_count": len(squares),
        "orientation_affine_count_distribution": counter_json(orientation_affine_counts),
        "orientation_affine_flag_stable_for_all_880": not unstable_square_indices,
        "unstable_orientation_square_indices": unstable_square_indices,
        "raw_oriented_affine_cell_labeling_count": raw_affine_oriented_count,
        "raw_oriented_non_affine_cell_labeling_count": raw_total - raw_affine_oriented_count,
        "raw_oriented_total": raw_total,
        "direct_value_complement_stable_count": len(direct_complement_stable),
        "canonical_value_complement_stable_count": len(canonical_complement_stable),
        "terminal24_pair_count": len(terminal_records),
        "terminal24_pair_d4_profile_stable": not unstable_terminal_records,
        "unstable_terminal24_records": unstable_terminal_records,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# F2 Orientation Stability Report",
        "",
        "Status: Phase F closing micro-audit",
        "",
        "## Summary",
        "",
        f"- all D4 domain transforms affine automorphisms: `{result['all_d4_domain_transforms_are_affine_automorphisms']}`",
        f"- essential squares: `{result['essential_square_count']}`",
        f"- orientation affine-count distribution: `{result['orientation_affine_count_distribution']}`",
        f"- affine flag stable for all 880 D4 orbits: `{result['orientation_affine_flag_stable_for_all_880']}`",
        f"- raw oriented affine/non-affine counts: `{result['raw_oriented_affine_cell_labeling_count']}` / `{result['raw_oriented_non_affine_cell_labeling_count']}`",
        f"- direct value-complement stable count: `{result['direct_value_complement_stable_count']}`",
        f"- canonical value-complement stable count: `{result['canonical_value_complement_stable_count']}`",
        f"- terminal-24 pairs checked: `{result['terminal24_pair_count']}`",
        f"- terminal-24 D4 pair profiles stable: `{result['terminal24_pair_d4_profile_stable']}`",
        "",
        "## Interpretation",
        "",
        "The affine cell-value criterion is stable under the 8 square symmetries",
        "used for essential canonicalization, because those symmetries act as",
        "affine automorphisms on the row/column bit domain.  It is also stable",
        "under value complement, both directly and after canonicalizing the",
        "complement.",
        "",
        "The fixed phrase `exact canonical V4` remains orientation wording: it",
        "names the canonical representative's terminal diagonal set.  The",
        "underlying affine cell-value criterion itself is orientation stable.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_orientation_stability_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "f2_orientation_stability.json"
        report_path = root / "results" / "F2_ORIENTATION_STABILITY_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "all_d4_domain_transforms_are_affine_automorphisms": result[
                "all_d4_domain_transforms_are_affine_automorphisms"
            ],
            "orientation_affine_count_distribution": result[
                "orientation_affine_count_distribution"
            ],
            "orientation_affine_flag_stable_for_all_880": result[
                "orientation_affine_flag_stable_for_all_880"
            ],
            "terminal24_pair_d4_profile_stable": result[
                "terminal24_pair_d4_profile_stable"
            ],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
