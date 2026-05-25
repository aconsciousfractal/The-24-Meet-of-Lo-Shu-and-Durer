"""Compare Phase-C endpoint structures with standard order-4 families.

The family labels used here are computational:

- associated: opposite cells sum to 17;
- complement-fixed: canonical(17-Q) = Q;
- panmagic: all wrap/broken diagonals sum to 34;
- local_2x2: all non-wrapping 2x2 blocks sum to 34;
- wrap_2x2: all wrapping 2x2 blocks sum to 34;
- most_perfect_proxy: panmagic and wrap_2x2.

The script does not import a literature classification; it records exact
finite counts in the internal 880-square dataset.
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
import analyze_order4_v4_subclass as v4
import inspect_order4_durer_cell as durer_cell
import enumerate_order4_endpoints as order4


Square = tuple[tuple[int, ...], ...]


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


def is_associated(square: Square) -> bool:
    return all(square[i][j] + square[3 - i][3 - j] == 17 for i in range(4) for j in range(4))


def complement_square(square: Square) -> Square:
    return tuple(tuple(17 - x for x in row) for row in square)


def broken_diagonal_sums(square: Square) -> tuple[int, ...]:
    main = tuple(sum(square[i][(i + offset) % 4] for i in range(4)) for offset in range(4))
    anti = tuple(sum(square[i][(offset - i) % 4] for i in range(4)) for offset in range(4))
    return main + anti


def is_panmagic(square: Square) -> bool:
    return all(total == 34 for total in broken_diagonal_sums(square))


def two_by_two_sums(square: Square, wrap: bool) -> tuple[int, ...]:
    range_i = range(4) if wrap else range(3)
    range_j = range(4) if wrap else range(3)
    return tuple(
        sum(square[(i + di) % 4][(j + dj) % 4] for di in (0, 1) for dj in (0, 1))
        for i in range_i
        for j in range_j
    )


def has_all_2x2_sum_34(square: Square, wrap: bool) -> bool:
    return all(total == 34 for total in two_by_two_sums(square, wrap))


def family_flags(square: Square, index_by_square: dict[Square, int], square_index: int) -> dict[str, bool]:
    complement_index = index_by_square[order4.canonical_square(complement_square(square))]
    panmagic = is_panmagic(square)
    wrap_2x2 = has_all_2x2_sum_34(square, wrap=True)
    return {
        "associated": is_associated(square),
        "complement_fixed": complement_index == square_index,
        "panmagic": panmagic,
        "local_2x2": has_all_2x2_sum_34(square, wrap=False),
        "wrap_2x2": wrap_2x2,
        "most_perfect_proxy": panmagic and wrap_2x2,
    }


@lru_cache(maxsize=1)
def compare_named_families() -> dict:
    squares = order4.essential_order4_representatives()
    index_by_square = {square: idx for idx, square in enumerate(squares)}
    flags = [family_flags(square, index_by_square, idx) for idx, square in enumerate(squares)]
    apd_by_square = [fp.apd_vector(square) for square in squares]
    source_type_by_set = {
        tuple(row["source_diagonal_set"]): row["type_id"]
        for row in v4.classify_v4_subclass()["source_diagonal_types"]
    }

    family_square_counts = Counter()
    family_endpoint_counts: dict[str, Counter] = {}
    family_exact_v4_records: dict[str, list[dict[str, Any]]] = {}
    family_names = list(flags[0])

    for name in family_names:
        family_square_counts[name] = sum(1 for row in flags if row[name])
        family_endpoint_counts[name] = Counter()
        family_exact_v4_records[name] = []

    for record in ladder.all_pair_records():
        square_index = record["square_index"]
        for name in family_names:
            if not flags[square_index][name]:
                continue
            family_endpoint_counts[name][record["terminal_sum"]] += 1
            if ladder.has_exact_v4_set(record):
                square = squares[square_index]
                enriched = dict(record)
                enriched["apd_vector"] = v4.apd_key(apd_by_square[square_index])
                enriched["source_diagonal_type"] = source_type_by_set.get(
                    fp.source_diagonal_set(square), "outside_v4_source_types"
                )
                family_exact_v4_records[name].append(enriched)

    combined_square_family_counts = Counter(
        tuple(name for name in family_names if row[name]) for row in flags
    )

    family_summaries = {}
    for name in family_names:
        exact = family_exact_v4_records[name]
        family_summaries[name] = {
            "square_count": family_square_counts[name],
            "pair_count": family_square_counts[name] * 8,
            "endpoint_distribution": counter_json(family_endpoint_counts[name]),
            "endpoint_24_pair_count": family_endpoint_counts[name][24],
            "exact_v4_pair_count": len(exact),
            "exact_v4_square_count": len({record["square_index"] for record in exact}),
            "exact_v4_mask_counts": counter_json(Counter(record["mask"] for record in exact)),
            "exact_v4_apd_counts": counter_json(Counter(record["apd_vector"] for record in exact)),
            "exact_v4_source_type_counts": counter_json(
                Counter(record["source_diagonal_type"] for record in exact)
            ),
            "exact_v4_square_indices": sorted(record["square_index"] for record in exact),
        }

    associated_exact = family_exact_v4_records["associated"]
    durer_indices = set(durer_cell.inspect_durer_cell()["cell"]["square_indices"])
    associated_durer_overlap = [
        record for record in associated_exact if record["square_index"] in durer_indices
    ]

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Comparison of endpoint structures with computational order-4 family labels.",
            "source_dataset": "data/order4_normal_essential_880.json",
        },
        "family_square_counts": counter_json(family_square_counts),
        "combined_square_family_counts": {
            ",".join(key) if key else "none": count
            for key, count in sorted(combined_square_family_counts.items(), key=lambda kv: str(kv[0]))
        },
        "family_summaries": family_summaries,
        "associated_exact_v4": {
            "pair_count": len(associated_exact),
            "square_count": len({record["square_index"] for record in associated_exact}),
            "apd_counts": counter_json(Counter(record["apd_vector"] for record in associated_exact)),
            "source_type_counts": counter_json(
                Counter(record["source_diagonal_type"] for record in associated_exact)
            ),
            "square_indices": sorted(record["square_index"] for record in associated_exact),
            "durer_cell_overlap_count": len(associated_durer_overlap),
            "durer_cell_overlap_square_indices": sorted(
                record["square_index"] for record in associated_durer_overlap
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write named-family comparison JSON")
    args = parser.parse_args()

    result = compare_named_families()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "order4_named_families.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = {
            "family_square_counts": result["family_square_counts"],
            "combined_square_family_counts": result["combined_square_family_counts"],
            "associated_exact_v4": result["associated_exact_v4"],
            "panmagic_summary": result["family_summaries"]["panmagic"],
            "most_perfect_proxy_summary": result["family_summaries"]["most_perfect_proxy"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
