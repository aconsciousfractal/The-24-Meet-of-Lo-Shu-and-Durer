"""Internal quotient table for the 144-pair canonical V4 subclass.

The exact canonical V4 subclass is already reduced by square symmetries in the
essential 880-square dataset.  The induced D4 action on these representatives
is therefore trivial.  The useful quotient at this stage is the internal
invariant quotient by:

- APD-style class;
- source permutation-diagonal type;
- mask.
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
import analyze_order4_v4_subclass as v4
import enumerate_order4_endpoints as order4


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


@lru_cache(maxsize=1)
def build_v4_quotient() -> dict:
    subclass = v4.classify_v4_subclass()
    records = [record for record in ladder.all_pair_records() if ladder.has_exact_v4_set(record)]
    squares = order4.essential_order4_representatives()
    apd_by_square = [fp.apd_vector(square) for square in squares]
    source_type_by_set = {
        tuple(row["source_diagonal_set"]): row["type_id"]
        for row in subclass["source_diagonal_types"]
    }

    cell_records: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        apd = v4.apd_key(apd_by_square[record["square_index"]])
        source_type = source_type_by_set[
            fp.source_diagonal_set(squares[record["square_index"]])
        ]
        cell_records[(apd, source_type)].append(record)

    cells = []
    for (apd, source_type), group in sorted(cell_records.items()):
        cells.append(
            {
                "apd_vector": apd,
                "source_diagonal_type": source_type,
                "pair_count": len(group),
                "square_count": len({record["square_index"] for record in group}),
                "mask_counts": counter_json(Counter(record["mask"] for record in group)),
                "square_indices": sorted(record["square_index"] for record in group),
            }
        )

    d_index = ladder.durer_canonical_index()
    durer_cell = next(
        cell
        for cell in cells
        if d_index in cell["square_indices"]
    )

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "APD x source-diagonal-type quotient for the 144-pair exact canonical V4 subclass.",
            "source_v4_subclass": "results/order4_v4_subclass.json",
        },
        "pair_count": len(records),
        "cell_count": len(cells),
        "cells": cells,
        "cell_size_distribution": counter_json(
            Counter(cell["pair_count"] for cell in cells)
        ),
        "d4_action_on_essential_pairs": {
            "is_trivial_after_canonicalization": True,
            "reason": "The dataset already quotients normal squares by the 8 square symmetries; transforming and re-canonicalizing a generic essential pair returns the same essential pair.",
        },
        "durer_cell": {
            "canonical_square_index": d_index,
            "apd_vector": durer_cell["apd_vector"],
            "source_diagonal_type": durer_cell["source_diagonal_type"],
            "pair_count": durer_cell["pair_count"],
            "mask_counts": durer_cell["mask_counts"],
            "square_indices": durer_cell["square_indices"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write V4 quotient JSON")
    args = parser.parse_args()

    result = build_v4_quotient()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "order4_v4_quotient.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = {
            "pair_count": result["pair_count"],
            "cell_count": result["cell_count"],
            "cell_size_distribution": result["cell_size_distribution"],
            "durer_cell": result["durer_cell"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
