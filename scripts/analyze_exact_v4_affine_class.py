"""Phase J audit for the exact-canonical V4 affine terminal subclass."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import analyze_order4_f2_extension as f2ext


CANONICAL_V4_KEY = "0123,1032,2301,3210"


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def terminal_set_key(profile: dict) -> str:
    return ",".join(sorted(profile["terminal_diagonal_set"]))


def bool_key(value: bool) -> str:
    return "true" if value else "false"


def build_exact_v4_affine_class_audit() -> dict:
    root = Path(__file__).resolve().parents[1]
    f2_result = f2ext.build_order4_f2_extension()
    orientation = f2ext.load_json(root / "results" / "f2_orientation_stability.json")
    profiles = f2_result["records"]

    split_counter = Counter()
    selected_affine_split = Counter()
    terminal_set_split = Counter()
    selected_values_split = Counter()

    exact_pairs = set()
    affine_cell_pairs = set()
    selected_affine_pairs = set()
    high_plane_pairs = set()
    extras = []

    for profile in profiles:
        pair = (profile["square_index"], profile["mask"])
        cell_affine = profile["cell_labeling"]["is_affine_automorphism"]
        selected_affine = profile["selected_mask_is_affine_plane"]
        exact_v4 = profile["is_exact_canonical_v4"]
        selected_values = tuple(profile["sorted_values"])
        high_plane = selected_values == (11, 12, 15, 16)
        terminal_key = terminal_set_key(profile)

        split_counter[(selected_affine, cell_affine, exact_v4)] += 1
        selected_values_split[(selected_values, selected_affine, cell_affine, exact_v4)] += 1
        terminal_set_split[(terminal_key, cell_affine, exact_v4)] += 1

        if exact_v4:
            exact_pairs.add(pair)
        if cell_affine:
            affine_cell_pairs.add(pair)
        if selected_affine:
            selected_affine_pairs.add(pair)
        if high_plane:
            high_plane_pairs.add(pair)
        if selected_affine and not cell_affine:
            extras.append(
                {
                    "square_index": profile["square_index"],
                    "mask": profile["mask"],
                    "terminal_diagonal_set": profile["terminal_diagonal_set"],
                    "sorted_values": list(profile["sorted_values"]),
                    "terminal_affine_count": profile["terminal_f2_profile"][
                        "terminal_affine_count"
                    ],
                    "pure_transport": profile["terminal_f2_profile"][
                        "terminal_affine_is_pure_transport"
                    ],
                }
            )

    exact_equals_cell_affine = exact_pairs == affine_cell_pairs
    selected_affine_equals_high_plane = selected_affine_pairs == high_plane_pairs
    exact_equals_selected_affine_and_cell_affine = exact_pairs == (
        selected_affine_pairs & affine_cell_pairs
    )

    selected_affine_extra_pairs = selected_affine_pairs - affine_cell_pairs
    selected_affine_split["cell_affine_exact_v4"] = len(
        selected_affine_pairs & affine_cell_pairs & exact_pairs
    )
    selected_affine_split["cell_non_affine_non_exact"] = len(selected_affine_extra_pairs)

    orientation_summary = {
        "affine_cell_value_criterion_stable_under_d4": orientation[
            "orientation_affine_flag_stable_for_all_880"
        ],
        "affine_cell_value_criterion_stable_under_complement": (
            orientation["direct_value_complement_stable_count"] == 880
            and orientation["canonical_value_complement_stable_count"] == 880
        ),
        "terminal24_pair_f2_profiles_stable_under_d4": orientation[
            "terminal24_pair_d4_profile_stable"
        ],
        "canonical_v4_wording_orientation_free": False,
    }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase J",
            "description": "Exact-canonical V4 affine-class audit on the 236 terminal-24 pairs.",
            "input": "results/order4_f2_extension.json and results/f2_orientation_stability.json",
        },
        "terminal24_pair_count": len(profiles),
        "exact_canonical_v4_pair_count": len(exact_pairs),
        "affine_cell_labeling_pair_count": len(affine_cell_pairs),
        "selected_mask_affine_pair_count": len(selected_affine_pairs),
        "high_plane_selected_values_pair_count": len(high_plane_pairs),
        "exact_canonical_v4_equals_affine_cell_labeling": exact_equals_cell_affine,
        "selected_mask_affine_equals_selected_values_11_12_15_16": (
            selected_affine_equals_high_plane
        ),
        "exact_canonical_v4_equals_selected_mask_affine_and_cell_affine": (
            exact_equals_selected_affine_and_cell_affine
        ),
        "phase_j_minimal_filter_ladder": {
            "terminal24": len(profiles),
            "selected_values_11_12_15_16_or_selected_mask_affine": len(
                selected_affine_pairs
            ),
            "plus_affine_cell_value_labeling": len(
                selected_affine_pairs & affine_cell_pairs
            ),
            "exact_canonical_v4": len(exact_pairs),
        },
        "main_176_split_by_cell_labeling": counter_json(selected_affine_split),
        "three_way_split_selected_mask_affine_cell_affine_exact_v4": counter_json(
            split_counter
        ),
        "selected_value_cell_affine_exact_v4_split": [
            {
                "sorted_values": ",".join(str(value) for value in key[0]),
                "selected_mask_affine": key[1],
                "cell_labeling_affine": key[2],
                "exact_canonical_v4": key[3],
                "pair_count": count,
            }
            for key, count in sorted(selected_values_split.items(), key=lambda item: item[0])
        ],
        "terminal_set_cell_affine_exact_v4_split": [
            {
                "terminal_diagonal_set": key[0],
                "cell_labeling_affine": key[1],
                "exact_canonical_v4": key[2],
                "pair_count": count,
            }
            for key, count in sorted(terminal_set_split.items(), key=lambda item: item[0])
        ],
        "selected_affine_non_cell_affine_extra_count": len(extras),
        "selected_affine_non_cell_affine_terminal_sets": counter_json(
            Counter(terminal_set_key(profile) for profile in profiles if (
                profile["selected_mask_is_affine_plane"]
                and not profile["cell_labeling"]["is_affine_automorphism"]
            ))
        ),
        "selected_affine_non_cell_affine_records": extras,
        "orientation_free_reading": orientation_summary,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Exact-V4 Affine Class Audit",
        "",
        "Status: Phase J finite characterization pass",
        "",
        "## Summary",
        "",
        f"- terminal-24 pairs: `{result['terminal24_pair_count']}`",
        f"- selected-mask affine / values `{{11,12,15,16}}`: `{result['selected_mask_affine_pair_count']}`",
        f"- affine cell-value labeling pairs: `{result['affine_cell_labeling_pair_count']}`",
        f"- exact canonical `V4` pairs: `{result['exact_canonical_v4_pair_count']}`",
        f"- exact canonical `V4` equals affine cell-value labeling: `{result['exact_canonical_v4_equals_affine_cell_labeling']}`",
        f"- selected-mask affine equals selected values `{{11,12,15,16}}`: `{result['selected_mask_affine_equals_selected_values_11_12_15_16']}`",
        f"- exact canonical `V4` equals selected-mask affine plus affine cell-value labeling: `{result['exact_canonical_v4_equals_selected_mask_affine_and_cell_affine']}`",
        "",
        "## Minimal Filter Ladder",
        "",
    ]
    for label, count in result["phase_j_minimal_filter_ladder"].items():
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(
        [
            "",
            "## Main 176 Split",
            "",
            f"`{result['main_176_split_by_cell_labeling']}`",
            "",
            "The selected-mask affine class has `176` pairs.  It splits as",
            "`144` affine cell-value labelings, all exact canonical `V4`, plus",
            "`32` non-affine cell-value labelings, none exact canonical `V4`.",
            "",
            "## Extra Terminal Sets",
            "",
            f"`{result['selected_affine_non_cell_affine_terminal_sets']}`",
            "",
            "## Orientation Reading",
            "",
        ]
    )
    orientation = result["orientation_free_reading"]
    for key, value in orientation.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Within the terminal-24 dataset, the strongest current Phase-J",
            "statement is a finite equivalence:",
            "",
            "```text",
            "exact canonical V4",
            "  <=> affine cell-value labeling",
            "  <=> selected-mask affine plus affine cell-value labeling",
            "```",
            "",
            "The first filter `selected-mask affine` is too broad: it is the",
            "`176`-pair main class.  The affine cell-value condition removes",
            "exactly the `32` structured extras.",
            "",
            "The affine cell-value criterion is stable under square symmetries",
            "and value complement, but the literal phrase `exact canonical V4`",
            "is still canonical-orientation wording.",
            "",
            "## Paper Consequence",
            "",
            "Do not delay paper v2 for a conceptual proof beyond this finite",
            "equivalence.  The result is strong enough as an appendix-backed",
            "finite theorem; a broader conceptual explanation belongs to a",
            "follow-up Type-A/subgroup-tiler project.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_exact_v4_affine_class_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "exact_v4_affine_class_audit.json"
        report_path = root / "results" / "EXACT_V4_AFFINE_CLASS_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "terminal24_pair_count": result["terminal24_pair_count"],
            "selected_mask_affine_pair_count": result["selected_mask_affine_pair_count"],
            "affine_cell_labeling_pair_count": result["affine_cell_labeling_pair_count"],
            "exact_canonical_v4_pair_count": result["exact_canonical_v4_pair_count"],
            "exact_canonical_v4_equals_affine_cell_labeling": result[
                "exact_canonical_v4_equals_affine_cell_labeling"
            ],
            "exact_canonical_v4_equals_selected_mask_affine_and_cell_affine": result[
                "exact_canonical_v4_equals_selected_mask_affine_and_cell_affine"
            ],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
