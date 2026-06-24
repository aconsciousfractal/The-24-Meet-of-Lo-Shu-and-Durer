"""Sagrada terminal retraction and count-shadow certificate.

This public replay supports the paper-safe Shu-Durer insertion.  It checks the
terminal square D(10) as a finite retraction of the Durer-complement source,
recovers the terminal duplicate-fiber direction u=1001, and records the guarded
nonaffine terminal-quaterne count vector 60=32+12+16.

The final count vector is a count-shadow only.  It is not a record/profile lift
and not an identification with any endpoint-24 atlas class.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_JSON = ROOT / "results" / "sagrada_terminal_retraction_shadow.json"
RESULT_REPORT = ROOT / "results" / "SAGRADA_TERMINAL_RETRACTION_SHADOW_REPORT.md"

DURER_COMPLEMENT = [
    [1, 14, 15, 4],
    [12, 7, 6, 9],
    [8, 11, 10, 5],
    [13, 2, 3, 16],
]

SAGRADA_MASK_CELLS = ((0, 2), (1, 0), (2, 1), (3, 3))
U = (1, 0, 0, 1)


def cell_bits(row: int, column: int) -> tuple[int, int, int, int]:
    return ((row >> 1) & 1, row & 1, (column >> 1) & 1, column & 1)


def cell_from_bits(bits: tuple[int, int, int, int]) -> tuple[int, int]:
    return (2 * bits[0] + bits[1], 2 * bits[2] + bits[3])


def xor_bits(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x ^ y for x, y in zip(a, b))


def bits_key(bits: tuple[int, ...]) -> str:
    return "".join(str(bit) for bit in bits)


def all_cells_bits() -> list[tuple[int, int, int, int]]:
    return [cell_bits(row, column) for row in range(4) for column in range(4)]


def matrix_value(matrix: list[list[int]], point: tuple[int, int, int, int]) -> int:
    row, column = cell_from_bits(point)
    return matrix[row][column]


def sagrada_plane_bits() -> set[tuple[int, int, int, int]]:
    return {cell_bits(row, column) for row, column in SAGRADA_MASK_CELLS}


def terminal_matrix_by_subtraction() -> list[list[int]]:
    out = [row[:] for row in DURER_COMPLEMENT]
    for row, column in SAGRADA_MASK_CELLS:
        out[row][column] -= 10
    return out


def fold_map(point: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    if point in sagrada_plane_bits():
        return xor_bits(point, U)  # type: ignore[return-value]
    return point


def terminal_matrix_by_retraction() -> list[list[int]]:
    out = [[0 for _ in range(4)] for _ in range(4)]
    for point in all_cells_bits():
        row, column = cell_from_bits(point)
        out[row][column] = matrix_value(DURER_COMPLEMENT, fold_map(point))
    return out


def fold_fibers() -> dict[str, list[str]]:
    fibers: dict[str, list[str]] = defaultdict(list)
    for point in all_cells_bits():
        fibers[bits_key(fold_map(point))].append(bits_key(point))
    return dict(sorted((key, sorted(value)) for key, value in fibers.items()))


def duplicate_fiber_rows(d10: list[list[int]]) -> list[dict[str, Any]]:
    locations: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for row, values in enumerate(d10):
        for column, value in enumerate(values):
            locations[value].append((row, column))

    rows = []
    for value in sorted(value for value, cells in locations.items() if len(cells) == 2):
        a, b = locations[value]
        a_bits = cell_bits(*a)
        b_bits = cell_bits(*b)
        rows.append({
            "value": value,
            "cells": [list(a), list(b)],
            "bits": [bits_key(a_bits), bits_key(b_bits)],
            "difference": bits_key(xor_bits(a_bits, b_bits)),
        })
    return rows


def add_many(points: tuple[tuple[int, int, int, int], ...]) -> tuple[int, int, int, int]:
    out = (0, 0, 0, 0)
    for point in points:
        out = xor_bits(out, point)  # type: ignore[assignment]
    return out


def is_affine_plane(points: tuple[tuple[int, int, int, int], ...]) -> bool:
    return len(points) == 4 and len(set(points)) == 4 and add_many(points) == (0, 0, 0, 0)


def terminal_quaternes(d10: list[list[int]]) -> list[tuple[tuple[int, int, int, int], ...]]:
    rows = []
    for q in combinations(all_cells_bits(), 4):
        if sum(matrix_value(d10, point) for point in q) == 24:
            rows.append(tuple(sorted(q, key=cell_from_bits)))
    return rows


def q_key(q: tuple[tuple[int, int, int, int], ...]) -> str:
    return " ".join(bits_key(point) for point in q)


def fold_pairs() -> list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]:
    return [(point, xor_bits(point, U)) for point in sorted(sagrada_plane_bits(), key=cell_from_bits)]  # type: ignore[list-item]


def apply_swap_mask(
    q: tuple[tuple[int, int, int, int], ...],
    swap_bits: tuple[int, int, int, int],
    pairs: list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]],
) -> tuple[tuple[int, int, int, int], ...]:
    cells = set(q)
    for bit, (left, right) in zip(swap_bits, pairs):
        if not bit:
            continue
        has_left = left in cells
        has_right = right in cells
        if has_left and not has_right:
            cells.remove(left)
            cells.add(right)
        elif has_right and not has_left:
            cells.remove(right)
            cells.add(left)
    return tuple(sorted(cells, key=cell_from_bits))


def orbit_type(size: int, affine_count: int, nonaffine_count: int) -> str:
    if size == 4 and affine_count == 2 and nonaffine_count == 2:
        return "size4_mixed_2A2N"
    if size == 2 and affine_count == 0 and nonaffine_count == 2:
        return "size2_pure_N2"
    if size == 1 and affine_count == 1 and nonaffine_count == 0:
        return "size1_pure_A"
    if size == 1 and affine_count == 0 and nonaffine_count == 1:
        return "size1_pure_N"
    return f"unexpected_size{size}_A{affine_count}_N{nonaffine_count}"


def orbit_decomposition(qs: list[tuple[tuple[int, int, int, int], ...]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    pairs = fold_pairs()
    q_set = set(qs)
    seen: set[tuple[tuple[int, int, int, int], ...]] = set()
    orbits = []
    q_to_orbit_type: dict[str, str] = {}
    for q in qs:
        if q in seen:
            continue
        orbit = {apply_swap_mask(q, mask, pairs) for mask in product((0, 1), repeat=4)}
        assert orbit <= q_set
        seen.update(orbit)
        affine_members = [member for member in orbit if is_affine_plane(member)]
        nonaffine_members = [member for member in orbit if not is_affine_plane(member)]
        kind = orbit_type(len(orbit), len(affine_members), len(nonaffine_members))
        for member in orbit:
            q_to_orbit_type[q_key(member)] = kind
        orbits.append({
            "representative": q_key(min(orbit, key=q_key)),
            "size": len(orbit),
            "affine_count": len(affine_members),
            "nonaffine_count": len(nonaffine_members),
            "orbit_type": kind,
        })
    return sorted(orbits, key=lambda row: (row["orbit_type"], row["representative"])), q_to_orbit_type


def canonical_mod_u(point: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    partner = xor_bits(point, U)
    return min(point, partner)  # type: ignore[return-value]


def shadow_family(q: tuple[tuple[int, int, int, int], ...], q_to_orbit_type: dict[str, str]) -> str:
    kind = q_to_orbit_type[q_key(q)]
    cell_xor = add_many(q)
    mod_u = bits_key(canonical_mod_u(cell_xor))
    if kind == "size4_mixed_2A2N" and cell_xor == U:
        return "CS1_mixed_single_direction"
    if kind in {"size2_pure_N2", "size1_pure_N"} and mod_u in {"0010", "0101"}:
        return "CS2_pure_nonfull_direction"
    if kind in {"size2_pure_N2", "size1_pure_N"} and mod_u == "0111":
        return "CS3_pure_full_direction"
    return "unclassified"


def build_certificate() -> dict[str, Any]:
    d10_sub = terminal_matrix_by_subtraction()
    d10_ret = terminal_matrix_by_retraction()
    fibers = fold_fibers()
    duplicate_rows = duplicate_fiber_rows(d10_sub)
    qs = terminal_quaternes(d10_sub)
    orbits, q_to_orbit_type = orbit_decomposition(qs)
    nonaffine = [q for q in qs if not is_affine_plane(q)]
    shadow_counts = Counter(shadow_family(q, q_to_orbit_type) for q in nonaffine)
    orbit_type_counts = Counter(row["orbit_type"] for row in orbits)
    duplicate_directions = sorted({row["difference"] for row in duplicate_rows})

    return {
        "square": "Durer-complement Sagrada terminal D(10)",
        "sagrada_mask": "2013",
        "fold_direction": bits_key(U),
        "fold_image_mask": "0231",
        "terminal_matrix": d10_sub,
        "retraction": {
            "subtraction_equals_retraction": d10_sub == d10_ret,
            "image_size": len(fibers),
            "fiber_size_distribution": dict(sorted(Counter(len(v) for v in fibers.values()).items())),
            "sagrada_plane": [bits_key(point) for point in sorted(sagrada_plane_bits(), key=cell_from_bits)],
            "fold_pairs": [
                {"from": bits_key(left), "to": bits_key(right), "from_cell": list(cell_from_bits(left)), "to_cell": list(cell_from_bits(right))}
                for left, right in fold_pairs()
            ],
        },
        "terminal_duplicate_direction": {
            "duplicate_values": [row["value"] for row in duplicate_rows],
            "duplicate_rows": duplicate_rows,
            "duplicate_directions": duplicate_directions,
            "terminally_recovered_direction": duplicate_directions[0] if len(duplicate_directions) == 1 else None,
        },
        "terminal_quaternes": {
            "h24_count": len(qs),
            "affine_count": sum(is_affine_plane(q) for q in qs),
            "nonaffine_count": len(nonaffine),
            "orbit_type_counts": dict(sorted(orbit_type_counts.items())),
            "shadow_count_vector": dict(sorted(shadow_counts.items())),
            "shadow_count_vector_numeric": [
                shadow_counts["CS1_mixed_single_direction"],
                shadow_counts["CS2_pure_nonfull_direction"],
                shadow_counts["CS3_pure_full_direction"],
            ],
        },
        "claims": {
            "terminal_is_retraction_of_source": d10_sub == d10_ret,
            "retraction_image_size_is_12": len(fibers) == 12,
            "duplicate_direction_is_terminally_recovered_u": duplicate_directions == [bits_key(U)],
            "h24_count_is_96": len(qs) == 96,
            "affine_nonaffine_split_is_36_60": (sum(is_affine_plane(q) for q in qs), len(nonaffine)) == (36, 60),
            "nonaffine_count_shadow_is_32_12_16": [
                shadow_counts["CS1_mixed_single_direction"],
                shadow_counts["CS2_pure_nonfull_direction"],
                shadow_counts["CS3_pure_full_direction"],
            ] == [32, 12, 16],
            "no_b3_identification_claim": True,
        },
        "guardrails": [
            "The 32/12/16 vector is a count-shadow only.",
            "The replay does not construct a record/profile lift to any endpoint-24 atlas class.",
            "The terminal square D(10) is non-normal and is not an endpoint-24 normal atlas record.",
        ],
    }


def write_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(data: dict[str, Any], path: Path) -> None:
    rows = [
        f"| {row['value']} | `{row['bits'][0]}` | `{row['bits'][1]}` | `{row['difference']}` |"
        for row in data["terminal_duplicate_direction"]["duplicate_rows"]
    ]
    text = "\n".join([
        "# Sagrada Terminal Retraction and Count Shadow",
        "",
        "Status: public replay artifact for the Shu-Durer paper.",
        "",
        "## Retraction",
        "",
        f"- fold direction: `{data['fold_direction']}`",
        f"- image size: `{data['retraction']['image_size']}`",
        f"- fiber-size distribution: `{data['retraction']['fiber_size_distribution']}`",
        f"- subtraction equals retraction: `{data['claims']['terminal_is_retraction_of_source']}`",
        "",
        "## Terminal Duplicate Direction",
        "",
        "| value | bits A | bits B | difference |",
        "|---:|---|---|---|",
        *rows,
        "",
        "## Terminal Quaternes",
        "",
        f"- `|H_24(D(10))| = {data['terminal_quaternes']['h24_count']}`",
        f"- affine/nonaffine split: `{data['terminal_quaternes']['affine_count']}/{data['terminal_quaternes']['nonaffine_count']}`",
        f"- nonaffine count-shadow vector: `{data['terminal_quaternes']['shadow_count_vector_numeric']}`",
        "",
        "## Guardrails",
        "",
        *[f"- {item}" for item in data["guardrails"]],
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write JSON and Markdown report")
    parser.add_argument("--json-out", type=Path, default=RESULT_JSON)
    parser.add_argument("--report-out", type=Path, default=RESULT_REPORT)
    args = parser.parse_args()
    data = build_certificate()
    if args.write:
        write_json(data, args.json_out)
        write_report(data, args.report_out)
        print(f"[wrote] {args.json_out}")
        print(f"[wrote] {args.report_out}")
    else:
        print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if all(data["claims"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())