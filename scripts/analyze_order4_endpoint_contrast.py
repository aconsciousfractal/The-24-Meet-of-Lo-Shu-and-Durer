"""Endpoint-by-endpoint contrast for the Phase-C order-4 dataset.

This script compares the terminal-24 fingerprints against every other endpoint
sum in the 880-square essential dataset.  It is the third Phase-C layer:

1. build the internal 880-square dataset;
2. isolate and fingerprint the 236 terminal-24 pairs;
3. compare those fingerprints against all non-24 endpoint pairs.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

import analyze_order4_terminal24 as fp
import enumerate_order4_endpoints as order4


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


def top_counter(counter: Counter, limit: int = 8) -> list[dict[str, Any]]:
    return [{"key": str(key), "count": count} for key, count in counter.most_common(limit)]


def ratio_text(numer: int, denom: int) -> str:
    return f"{numer}/{denom}"


@lru_cache(maxsize=1)
def classify_endpoint_contrast() -> dict:
    squares = order4.essential_order4_representatives()
    masks = order4.admissible_one_incidence_perms()

    apd_by_square = [fp.apd_vector(square) for square in squares]
    apd_all_classes = set(apd_by_square)

    by_sum: dict[int, dict[str, Any]] = {}
    endpoint_apd_classes: dict[int, set[tuple[int, int, int, int]]] = defaultdict(set)
    terminal_set_by_sum: dict[int, Counter] = defaultdict(Counter)

    for square_index, square in enumerate(squares):
        apd = apd_by_square[square_index]
        for mask in masks:
            endpoint = order4.endpoint_for_mask(square, mask)
            terminal_sum = endpoint["terminal_sum"]
            t = endpoint["t_max"]
            selected = fp.selected_values(square, mask)
            sorted_selected = tuple(sorted(selected))
            terminal_diags = fp.terminal_diagonal_set(square, mask, t)
            terminal_perm_set = {fp.perm_from_string(p) for p in terminal_diags}
            terminal_is_subgroup = fp.is_subgroup(terminal_perm_set)
            q = fp.source_quaterne_decomposition(square, mask, t)

            if terminal_sum not in by_sum:
                by_sum[terminal_sum] = {
                    "pair_count": 0,
                    "square_indices": set(),
                    "selected_value_signature_counts": Counter(),
                    "terminal_diagonal_size_counts": Counter(),
                    "terminal_diagonal_subgroup_counts": Counter(),
                    "terminal_diagonal_order_profile_counts": Counter(),
                    "terminal_quaterne_count_distribution": Counter(),
                    "terminal_decomposition_type_counts": Counter(),
                }

            bucket = by_sum[terminal_sum]
            bucket["pair_count"] += 1
            bucket["square_indices"].add(square_index)
            bucket["selected_value_signature_counts"][sorted_selected] += 1
            bucket["terminal_diagonal_size_counts"][len(terminal_diags)] += 1
            bucket["terminal_diagonal_subgroup_counts"][str(terminal_is_subgroup)] += 1
            if terminal_is_subgroup:
                bucket["terminal_diagonal_order_profile_counts"][
                    fp.order_profile(terminal_perm_set)
                ] += 1
            bucket["terminal_quaterne_count_distribution"][q["terminal_count"]] += 1
            bucket["terminal_decomposition_type_counts"][
                tuple(q["terminal_decomposition"].items())
            ] += 1
            endpoint_apd_classes[terminal_sum].add(apd)
            terminal_set_by_sum[terminal_sum][terminal_diags] += 1

    apd_classes_outside_24 = set()
    for terminal_sum, classes in endpoint_apd_classes.items():
        if terminal_sum != 24:
            apd_classes_outside_24.update(classes)

    endpoint_sections = {}
    for terminal_sum in sorted(by_sum):
        bucket = by_sum[terminal_sum]
        subgroup_counts = bucket["terminal_diagonal_subgroup_counts"]
        profile_counts = bucket["terminal_diagonal_order_profile_counts"]
        quaterne_counts = bucket["terminal_quaterne_count_distribution"]
        endpoint_sections[str(terminal_sum)] = {
            "pair_count": bucket["pair_count"],
            "square_count": len(bucket["square_indices"]),
            "apd_class_count": len(endpoint_apd_classes[terminal_sum]),
            "selected_value_signature_counts_top": top_counter(
                bucket["selected_value_signature_counts"]
            ),
            "terminal_diagonal_size_counts": counter_json(
                bucket["terminal_diagonal_size_counts"]
            ),
            "terminal_diagonal_subgroup_counts": counter_json(subgroup_counts),
            "terminal_diagonal_subgroup_ratio": ratio_text(
                subgroup_counts["True"], bucket["pair_count"]
            ),
            "terminal_diagonal_order_profile_counts": counter_json(profile_counts),
            "klein_four_profile_ratio": ratio_text(
                profile_counts["1:1,2:3"], bucket["pair_count"]
            ),
            "terminal_quaterne_count_distribution": counter_json(quaterne_counts),
            "quaterne_96_ratio": ratio_text(quaterne_counts[96], bucket["pair_count"]),
            "terminal_decomposition_type_count": len(
                bucket["terminal_decomposition_type_counts"]
            ),
            "top_terminal_diagonal_sets": [
                {
                    "terminal_diagonal_set": list(diags),
                    "count": count,
                    "is_subgroup": fp.is_subgroup(
                        {fp.perm_from_string(p) for p in diags}
                    ),
                }
                for diags, count in terminal_set_by_sum[terminal_sum].most_common(5)
            ],
        }

    terminal_24 = endpoint_sections["24"]
    non24_pair_count = sum(
        section["pair_count"]
        for terminal_sum, section in endpoint_sections.items()
        if terminal_sum != "24"
    )
    non24_subgroup_true = sum(
        int(section["terminal_diagonal_subgroup_counts"].get("True", 0))
        for terminal_sum, section in endpoint_sections.items()
        if terminal_sum != "24"
    )
    non24_klein_four = sum(
        int(section["terminal_diagonal_order_profile_counts"].get("1:1,2:3", 0))
        for terminal_sum, section in endpoint_sections.items()
        if terminal_sum != "24"
    )
    non24_quaterne_96 = sum(
        int(section["terminal_quaterne_count_distribution"].get("96", 0))
        for terminal_sum, section in endpoint_sections.items()
        if terminal_sum != "24"
    )

    unique_apd_24 = endpoint_apd_classes[24] - apd_classes_outside_24

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Endpoint-by-endpoint structural contrast over the 880 essential order-4 squares and 8 admissible masks.",
            "source_dataset": "data/order4_normal_essential_880.json",
            "source_endpoint_spectrum": "results/order4_endpoint_spectrum.json",
        },
        "total_pair_count": sum(section["pair_count"] for section in endpoint_sections.values()),
        "endpoint_count": len(endpoint_sections),
        "apd_class_count_all_squares": len(apd_all_classes),
        "by_terminal_sum": endpoint_sections,
        "terminal_24_vs_non24": {
            "pair_count": {
                "terminal_24": terminal_24["pair_count"],
                "non24": non24_pair_count,
            },
            "terminal_diagonal_subgroup": {
                "terminal_24": terminal_24["terminal_diagonal_subgroup_ratio"],
                "non24": ratio_text(non24_subgroup_true, non24_pair_count),
            },
            "klein_four_profile": {
                "terminal_24": terminal_24["klein_four_profile_ratio"],
                "non24": ratio_text(non24_klein_four, non24_pair_count),
            },
            "quaterne_96": {
                "terminal_24": terminal_24["quaterne_96_ratio"],
                "non24": ratio_text(non24_quaterne_96, non24_pair_count),
            },
            "apd_classes": {
                "terminal_24": len(endpoint_apd_classes[24]),
                "outside_24": len(apd_classes_outside_24),
                "unique_to_24": len(unique_apd_24),
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write endpoint contrast JSON")
    args = parser.parse_args()

    result = classify_endpoint_contrast()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "order4_endpoint_contrast.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = {
            "total_pair_count": result["total_pair_count"],
            "endpoint_count": result["endpoint_count"],
            "terminal_24_vs_non24": result["terminal_24_vs_non24"],
            "terminal_24": result["by_terminal_sum"]["24"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
