"""Phase O2 audit of the global affine normal order-4 layer."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import analyze_exact_v4_affine_mechanism as mechanism
import analyze_order4_f2_extension as f2ext
import enumerate_order4_endpoints as order4


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def selected_values_key(values: list[int]) -> str:
    return ",".join(str(value) for value in sorted(values))


def direction_key(direction: tuple[int, ...] | None) -> str:
    if direction is None:
        return "non_affine"
    return ",".join(str(value) for value in direction)


def permutation_words() -> list[str]:
    return [
        "".join(str(value) for value in permutation)
        for permutation in itertools.permutations(range(4))
    ]


def diagonal_sum(
    square: tuple[tuple[int, ...], ...],
    word: str,
    mask_word: str,
    t: int,
) -> int:
    total = 0
    for row, char in enumerate(word):
        col = int(char)
        value = square[row][col]
        if col == int(mask_word[row]):
            value -= t
        total += value
    return total


def build_affine_normal_layer() -> dict:
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]
    masks = order4.admissible_one_incidence_perms()
    words = permutation_words()

    affine_square_indices = []
    selected_plane_counter = Counter()
    direction_counter = Counter()
    endpoint_counter = Counter()
    endpoint_selected_plane_counter = Counter()
    terminal_set_counter = Counter()
    endpoint_full_translation_counter = Counter()
    records = []

    for square_index, square in enumerate(squares):
        cell_profile = f2ext.cell_labeling_affine_profile(
            [list(row) for row in square]
        )
        if not cell_profile["is_affine_automorphism"]:
            continue
        affine_square_indices.append(square_index)

        for mask in masks:
            mask_word = order4.perm_string(mask)
            selected_values = [square[row][mask[row]] for row in range(4)]
            selected_labels = [value - 1 for value in selected_values]
            selected_direction = f2ext.plane_direction(selected_labels)
            t_max = min(value - 1 for value in selected_values)
            endpoint = 34 - t_max
            terminal_set = tuple(
                sorted(
                    word
                    for word in words
                    if diagonal_sum(square, word, mask_word, t_max) == endpoint
                )
            )
            terminal_profile = mechanism.terminal_set_profile(list(terminal_set))

            values_key = selected_values_key(selected_values)
            dir_key = direction_key(selected_direction)
            full_translation = terminal_profile["is_full_translation_v4"]

            selected_plane_counter[values_key] += 1
            direction_counter[dir_key] += 1
            endpoint_counter[endpoint] += 1
            endpoint_selected_plane_counter[(endpoint, values_key, full_translation)] += 1
            terminal_set_counter[(endpoint, ",".join(terminal_set))] += 1
            endpoint_full_translation_counter[(endpoint, full_translation)] += 1

            records.append(
                {
                    "square_index": square_index,
                    "mask": mask_word,
                    "selected_values": sorted(selected_values),
                    "selected_labels": sorted(selected_labels),
                    "selected_direction": list(selected_direction)
                    if selected_direction
                    else None,
                    "t_max": t_max,
                    "endpoint": endpoint,
                    "terminal_set": list(terminal_set),
                    "terminal_set_is_full_translation_v4": full_translation,
                }
            )

    selected_plane_counts = list(selected_plane_counter.values())
    direction_counts = list(direction_counter.values())
    terminal24_records = [record for record in records if record["endpoint"] == 24]

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O2",
            "description": "Global affine normal order-4 layer audit across all 880 essential representatives and 8 one-incidence masks.",
        },
        "essential_square_count": len(squares),
        "affine_square_count": len(affine_square_indices),
        "non_affine_square_count": len(squares) - len(affine_square_indices),
        "affine_square_mask_pair_count": len(records),
        "selected_value_plane_count": len(selected_plane_counter),
        "selected_value_plane_count_distribution": counter_json(
            Counter(selected_plane_counts)
        ),
        "selected_value_plane_counts": counter_json(selected_plane_counter),
        "selected_direction_count": len(direction_counter),
        "selected_direction_count_distribution": counter_json(Counter(direction_counts)),
        "selected_direction_counts": counter_json(direction_counter),
        "endpoint_distribution_affine_layer": counter_json(endpoint_counter),
        "endpoint_selected_plane_full_translation_counts": [
            {
                "endpoint": endpoint,
                "selected_values": values_key,
                "terminal_set_is_full_translation_v4": full_translation,
                "pair_count": count,
            }
            for (endpoint, values_key, full_translation), count in sorted(
                endpoint_selected_plane_counter.items(), key=lambda item: item[0]
            )
        ],
        "endpoint_full_translation_counts": [
            {
                "endpoint": endpoint,
                "terminal_set_is_full_translation_v4": full_translation,
                "pair_count": count,
            }
            for (endpoint, full_translation), count in sorted(
                endpoint_full_translation_counter.items(), key=lambda item: item[0]
            )
        ],
        "terminal24_affine_layer_pair_count": len(terminal24_records),
        "terminal24_selected_value_planes": counter_json(
            Counter(selected_values_key(record["selected_values"]) for record in terminal24_records)
        ),
        "terminal24_terminal_sets": counter_json(
            Counter(",".join(record["terminal_set"]) for record in terminal24_records)
        ),
        "terminal24_all_full_translation_v4": all(
            record["terminal_set_is_full_translation_v4"]
            for record in terminal24_records
        ),
        "uniformity_reading": {
            "all_selected_value_planes_have_144_pairs": set(selected_plane_counts)
            == {144},
            "six_selected_directions_have_576_pairs_each": set(direction_counts)
            == {576},
            "terminal24_is_single_selected_value_plane": (
                Counter(selected_values_key(record["selected_values"]) for record in terminal24_records)
                == {"11,12,15,16": 144}
            ),
            "terminal24_in_affine_layer_is_exactly_full_translation_v4": all(
                record["terminal_set_is_full_translation_v4"]
                for record in terminal24_records
            ),
        },
        "records": records,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Affine Normal Order-4 Layer Audit",
        "",
        "Status: Phase O2 generalization pass",
        "",
        "## Scope",
        "",
        "This audit leaves the terminal-24 atlas and studies all globally",
        "affine essential normal order-4 representatives across all eight",
        "one-incidence masks.",
        "",
        "## Counts",
        "",
        f"- essential representatives: `{result['essential_square_count']}`",
        f"- globally affine representatives: `{result['affine_square_count']}`",
        f"- affine square-mask pairs: `{result['affine_square_mask_pair_count']}`",
        f"- selected value planes: `{result['selected_value_plane_count']}`",
        f"- selected directions: `{result['selected_direction_count']}`",
        "",
        "## Uniformity",
        "",
        f"- selected value plane count distribution: `{result['selected_value_plane_count_distribution']}`",
        f"- selected direction count distribution: `{result['selected_direction_count_distribution']}`",
        "",
        "Thus the `3456` affine square-mask pairs split uniformly as",
        "",
        "```text",
        "24 selected value planes x 144 pairs.",
        "```",
        "",
        "## Endpoint-24 Layer",
        "",
        f"- terminal-24 affine pairs: `{result['terminal24_affine_layer_pair_count']}`",
        f"- terminal-24 selected value planes: `{result['terminal24_selected_value_planes']}`",
        f"- terminal-24 terminal sets: `{result['terminal24_terminal_sets']}`",
        f"- terminal-24 all full translation V4: `{result['terminal24_all_full_translation_v4']}`",
        "",
        "So the `144` exact-`V4` records arise as one selected value plane",
        "inside the global affine normal layer:",
        "",
        "```text",
        "selected values {11,12,15,16}",
        "  -> endpoint 24",
        "  -> full translation terminal V4.",
        "```",
        "",
        "## Interpretation",
        "",
        "This is the first explanation of the number `144` beyond the",
        "terminal-24 atlas: among globally affine normal order-4 squares,",
        "the admissible masks distribute uniformly over `24` selected value",
        "planes.  The terminal-24 plane is exactly one of them.",
        "",
        "## Guardrail",
        "",
        "This is still a finite normal-order-4 statement.  It does not prove",
        "a universal endpoint theorem and it does not include non-affine",
        "terminal-24 records.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_affine_normal_layer()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "affine_normal_layer.json"
        report_path = root / "results" / "AFFINE_NORMAL_LAYER_REPORT.md"
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
