"""Classify the 144-pair canonical V4 subclass.

This is the fourth Phase-C layer.  The filter ladder isolates a 144-pair
subclass:

- endpoint 24;
- Klein-four terminal diagonal order profile;
- terminal quaterne count 96;
- exact terminal set {0123,1032,2301,3210}.

This script classifies that subclass by APD-style class, mask, source
permutation-diagonal type, and quaterne decomposition.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

import analyze_order4_filter_ladder as ladder
import analyze_order4_terminal24 as fp
import enumerate_order4_endpoints as order4


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


def apd_key(apd: tuple[int, int, int, int]) -> str:
    return "(" + ",".join(str(x) for x in apd) + ")"


def decomposition_key(record: dict[str, Any]) -> str:
    return "; ".join(
        f"{name}:{count}" for name, count in record["terminal_decomposition"].items()
    )


@lru_cache(maxsize=1)
def classify_v4_subclass() -> dict:
    records = [record for record in ladder.all_pair_records() if ladder.has_exact_v4_set(record)]
    squares = order4.essential_order4_representatives()
    apd_by_square = [fp.apd_vector(square) for square in squares]

    mask_counts = Counter(record["mask"] for record in records)
    apd_records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_set_records: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    decomposition_counts = Counter(decomposition_key(record) for record in records)

    for record in records:
        square = squares[record["square_index"]]
        apd_records[apd_key(apd_by_square[record["square_index"]])].append(record)
        source_set_records[fp.source_diagonal_set(square)].append(record)

    apd_classes = []
    for apd, group in sorted(apd_records.items()):
        apd_classes.append(
            {
                "apd_vector": apd,
                "pair_count": len(group),
                "square_count": len({record["square_index"] for record in group}),
                "representative_square_index": min(record["square_index"] for record in group),
                "mask_counts": counter_json(Counter(record["mask"] for record in group)),
                "source_diagonal_size_counts": counter_json(
                    Counter(
                        len(fp.source_diagonal_set(squares[record["square_index"]]))
                        for record in group
                    )
                ),
            }
        )

    source_diagonal_types = []
    for idx, (source_set, group) in enumerate(
        sorted(source_set_records.items(), key=lambda item: (-len(item[1]), item[0])), start=1
    ):
        source_diagonal_types.append(
            {
                "type_id": f"S{idx}",
                "source_diagonal_set": list(source_set),
                "source_diagonal_size": len(source_set),
                "pair_count": len(group),
                "square_count": len({record["square_index"] for record in group}),
                "mask_counts": counter_json(Counter(record["mask"] for record in group)),
                "apd_counts": counter_json(
                    Counter(apd_key(apd_by_square[record["square_index"]]) for record in group)
                ),
            }
        )

    d_index = ladder.durer_canonical_index()
    durer_record = [record for record in records if record["square_index"] == d_index][0]
    durer_apd = apd_key(apd_by_square[d_index])
    durer_source_set = fp.source_diagonal_set(squares[d_index])
    durer_source_type = next(
        row["type_id"]
        for row in source_diagonal_types
        if tuple(row["source_diagonal_set"]) == durer_source_set
    )

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Classification of the 144-pair exact canonical V4 endpoint-24 subclass.",
            "source_filter_ladder": "results/order4_filter_ladder.json",
        },
        "pair_count": len(records),
        "square_count": len({record["square_index"] for record in records}),
        "mask_counts": counter_json(mask_counts),
        "apd_class_count": len(apd_classes),
        "apd_classes": apd_classes,
        "source_diagonal_type_count": len(source_diagonal_types),
        "source_diagonal_types": source_diagonal_types,
        "terminal_decomposition_type_count": len(decomposition_counts),
        "terminal_decomposition_counts": counter_json(decomposition_counts),
        "durer": {
            "canonical_square_index": d_index,
            "mask": durer_record["mask"],
            "apd_vector": durer_apd,
            "source_diagonal_type": durer_source_type,
            "record": durer_record,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write V4 subclass JSON")
    args = parser.parse_args()

    result = classify_v4_subclass()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "order4_v4_subclass.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = {
            "pair_count": result["pair_count"],
            "square_count": result["square_count"],
            "mask_counts": result["mask_counts"],
            "apd_class_count": result["apd_class_count"],
            "source_diagonal_type_count": result["source_diagonal_type_count"],
            "terminal_decomposition_type_count": result["terminal_decomposition_type_count"],
            "durer": result["durer"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
