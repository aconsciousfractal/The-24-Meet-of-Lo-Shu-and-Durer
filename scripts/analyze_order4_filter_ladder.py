"""Filter-ladder analysis for the Phase-C endpoint-24 signal.

The endpoint contrast showed that endpoint 24 is not characterized by a single
invariant.  This script intersects the enriched filters:

- terminal endpoint 24;
- subgroup terminal permutation diagonals;
- Klein-four terminal order profile;
- terminal quaterne count 96.

It also locates the canonical Durer/Sagrada representative inside the ladder.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

import analyze_order4_terminal24 as fp
import enumerate_order4_endpoints as order4


DURER_COMPLEMENT = (
    (1, 14, 15, 4),
    (12, 7, 6, 9),
    (8, 11, 10, 5),
    (13, 2, 3, 16),
)


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


def record_for_pair(square_index: int, square: fp.Square, mask: fp.Perm) -> dict[str, Any]:
    endpoint = order4.endpoint_for_mask(square, mask)
    t = endpoint["t_max"]
    values = fp.selected_values(square, mask)
    terminal_diags = fp.terminal_diagonal_set(square, mask, t)
    terminal_perm_set = {fp.perm_from_string(p) for p in terminal_diags}
    terminal_is_subgroup = fp.is_subgroup(terminal_perm_set)
    quaternes = fp.source_quaterne_decomposition(square, mask, t)
    return {
        "square_index": square_index,
        "mask": fp.perm_string(mask),
        "terminal_sum": endpoint["terminal_sum"],
        "t_max": t,
        "values": list(values),
        "sorted_values": list(sorted(values)),
        "terminal_diagonal_set": list(terminal_diags),
        "terminal_diagonal_is_subgroup": terminal_is_subgroup,
        "terminal_diagonal_order_profile": (
            fp.order_profile(terminal_perm_set) if terminal_is_subgroup else None
        ),
        "terminal_quaterne_count": quaternes["terminal_count"],
        "terminal_decomposition": quaternes["terminal_decomposition"],
    }


@lru_cache(maxsize=1)
def all_pair_records() -> tuple[dict[str, Any], ...]:
    records = []
    squares = order4.essential_order4_representatives()
    for square_index, square in enumerate(squares):
        for mask in order4.admissible_one_incidence_perms():
            records.append(record_for_pair(square_index, square, mask))
    return tuple(records)


def has_endpoint_24(record: dict[str, Any]) -> bool:
    return record["terminal_sum"] == 24


def has_subgroup_terminal_diagonals(record: dict[str, Any]) -> bool:
    return has_endpoint_24(record) and record["terminal_diagonal_is_subgroup"]


def has_klein_four_profile(record: dict[str, Any]) -> bool:
    return (
        has_subgroup_terminal_diagonals(record)
        and record["terminal_diagonal_order_profile"] == "1:1,2:3"
    )


def has_quaterne_96(record: dict[str, Any]) -> bool:
    return has_klein_four_profile(record) and record["terminal_quaterne_count"] == 96


def has_durer_value_signature(record: dict[str, Any]) -> bool:
    return has_quaterne_96(record) and tuple(record["sorted_values"]) == (11, 12, 15, 16)


def has_exact_v4_set(record: dict[str, Any]) -> bool:
    return has_quaterne_96(record) and tuple(record["terminal_diagonal_set"]) == (
        "0123",
        "1032",
        "2301",
        "3210",
    )


def stage_summary(
    name: str,
    records: tuple[dict[str, Any], ...],
    predicate: Callable[[dict[str, Any]], bool],
) -> dict[str, Any]:
    selected = [record for record in records if predicate(record)]
    return {
        "name": name,
        "pair_count": len(selected),
        "square_count": len({record["square_index"] for record in selected}),
        "mask_counts": counter_json(Counter(record["mask"] for record in selected)),
        "selected_value_signature_counts": counter_json(
            Counter(tuple(record["sorted_values"]) for record in selected)
        ),
        "terminal_diagonal_set_counts": [
            {"terminal_diagonal_set": list(diags), "count": count}
            for diags, count in Counter(
                tuple(record["terminal_diagonal_set"]) for record in selected
            ).most_common()
        ],
        "terminal_quaterne_count_distribution": counter_json(
            Counter(record["terminal_quaterne_count"] for record in selected)
        ),
    }


def durer_canonical_index() -> int:
    reps = order4.essential_order4_representatives()
    return reps.index(order4.canonical_square(DURER_COMPLEMENT))


@lru_cache(maxsize=1)
def build_filter_ladder() -> dict:
    records = all_pair_records()
    stages: list[tuple[str, Callable[[dict[str, Any]], bool]]] = [
        ("all_pairs", lambda record: True),
        ("endpoint_24", has_endpoint_24),
        ("endpoint_24_and_subgroup_terminal_diagonals", has_subgroup_terminal_diagonals),
        ("endpoint_24_and_klein_four_profile", has_klein_four_profile),
        ("endpoint_24_and_klein_four_and_quaterne_96", has_quaterne_96),
        (
            "endpoint_24_and_klein_four_and_quaterne_96_and_values_11_12_15_16",
            has_durer_value_signature,
        ),
        ("same_filters_and_exact_canonical_v4_set", has_exact_v4_set),
    ]
    stage_summaries = [
        stage_summary(name, records, predicate) for name, predicate in stages
    ]

    d_index = durer_canonical_index()
    durer_records = [record for record in records if record["square_index"] == d_index]
    durer_terminal_record = [record for record in durer_records if record["terminal_sum"] == 24]

    strict_records = [record for record in records if has_quaterne_96(record)]
    exact_v4_records = [record for record in records if has_exact_v4_set(record)]

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Filter ladder for the enriched endpoint-24 structural signal.",
            "source_dataset": "data/order4_normal_essential_880.json",
        },
        "stage_summaries": stage_summaries,
        "strict_filter_pair_count": len(strict_records),
        "strict_filter_square_count": len({record["square_index"] for record in strict_records}),
        "exact_v4_pair_count": len(exact_v4_records),
        "exact_v4_square_count": len({record["square_index"] for record in exact_v4_records}),
        "durer_canonical_index": d_index,
        "durer_records": durer_records,
        "durer_terminal_record": durer_terminal_record[0] if durer_terminal_record else None,
        "strict_filter_contains_durer": any(record["square_index"] == d_index for record in strict_records),
        "exact_v4_filter_contains_durer": any(
            record["square_index"] == d_index for record in exact_v4_records
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write filter-ladder JSON")
    args = parser.parse_args()

    result = build_filter_ladder()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "order4_filter_ladder.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = {
            "stage_counts": [
                {
                    "name": stage["name"],
                    "pair_count": stage["pair_count"],
                    "square_count": stage["square_count"],
                }
                for stage in result["stage_summaries"]
            ],
            "durer_canonical_index": result["durer_canonical_index"],
            "durer_terminal_record": result["durer_terminal_record"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
