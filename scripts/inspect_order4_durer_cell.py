"""Inspect the 8-pair quotient cell containing Durer/Sagrada.

The V4 quotient reduces the finite neighborhood of the canonical
Durer/Sagrada representative to an 8-pair cell:

- APD vector (0,0,0,55296);
- source diagonal type S3;
- exact terminal V4 set;
- terminal quaterne decomposition 25+50+21.

This script records the square-by-square details of that cell.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

import analyze_order4_filter_ladder as ladder
import analyze_order4_terminal24 as fp
import analyze_order4_v4_quotient as quotient
import enumerate_order4_endpoints as order4


def matrix_to_lists(square: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    return [list(row) for row in square]


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


def is_associated(square: tuple[tuple[int, ...], ...]) -> bool:
    return all(square[i][j] + square[3 - i][3 - j] == 17 for i in range(4) for j in range(4))


def complement_square(square: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(17 - x for x in row) for row in square)


def broken_diagonal_profile(square: tuple[tuple[int, ...], ...]) -> dict[str, list[int]]:
    return {
        "main_wrap": [sum(square[i][(i + offset) % 4] for i in range(4)) for offset in range(4)],
        "anti_wrap": [sum(square[i][(offset - i) % 4] for i in range(4)) for offset in range(4)],
    }


def two_by_two_block_profile(square: tuple[tuple[int, ...], ...]) -> list[int]:
    return sorted(
        sum(square[i + di][j + dj] for di in (0, 1) for dj in (0, 1))
        for i in range(3)
        for j in range(3)
    )


@lru_cache(maxsize=1)
def inspect_durer_cell() -> dict:
    q = quotient.build_v4_quotient()
    square_indices = q["durer_cell"]["square_indices"]
    square_index_set = set(square_indices)
    reps = order4.essential_order4_representatives()
    index_by_square = {square: idx for idx, square in enumerate(reps)}
    cell_records = [
        record
        for record in ladder.all_pair_records()
        if record["square_index"] in square_index_set and ladder.has_exact_v4_set(record)
    ]
    cell_records.sort(key=lambda record: (record["square_index"], record["mask"]))

    rows = []
    for record in cell_records:
        idx = record["square_index"]
        square = reps[idx]
        complement_idx = index_by_square[order4.canonical_square(complement_square(square))]
        rows.append(
            {
                "square_index": idx,
                "mask": record["mask"],
                "square": matrix_to_lists(square),
                "values": record["values"],
                "is_durer_canonical": idx == q["durer_cell"]["canonical_square_index"],
                "is_associated_opposite_sum_17": is_associated(square),
                "complement_canonical_index": complement_idx,
                "complement_fixed_after_canonicalization": complement_idx == idx,
                "broken_diagonal_profile": broken_diagonal_profile(square),
                "two_by_two_block_profile": two_by_two_block_profile(square),
                "terminal_decomposition": record["terminal_decomposition"],
            }
        )

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Square-by-square inspection of the 8-pair Durer/Sagrada quotient cell.",
            "source_v4_quotient": "results/order4_v4_quotient.json",
        },
        "cell": q["durer_cell"],
        "pair_count": len(rows),
        "square_count": len({row["square_index"] for row in rows}),
        "mask_counts": counter_json(Counter(row["mask"] for row in rows)),
        "associated_count": sum(row["is_associated_opposite_sum_17"] for row in rows),
        "complement_fixed_count": sum(row["complement_fixed_after_canonicalization"] for row in rows),
        "broken_diagonal_profile_counts": counter_json(
            Counter(
                (
                    tuple(row["broken_diagonal_profile"]["main_wrap"]),
                    tuple(row["broken_diagonal_profile"]["anti_wrap"]),
                )
                for row in rows
            )
        ),
        "two_by_two_block_profile_counts": counter_json(
            Counter(tuple(row["two_by_two_block_profile"]) for row in rows)
        ),
        "records": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write Durer-cell inspection JSON")
    args = parser.parse_args()

    result = inspect_durer_cell()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "order4_durer_cell.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = dict(result)
        summary["records_sample"] = summary["records"][:2]
        summary["records"] = f"{len(result['records'])} records omitted; run with --write for full JSON"
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
