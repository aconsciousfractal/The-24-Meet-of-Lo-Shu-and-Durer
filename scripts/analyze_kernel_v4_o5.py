"""Phase O5 audit of the value-bit kernel V4 versus terminal translation V4."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import analyze_affine_normal_count_derivation as count_derivation
import analyze_affine_normal_layer as affine_layer
import analyze_order4_f2_extension as f2ext


AXES = (8, 4, 2, 1)
MATCHINGS = (
    ((8, 4), (2, 1)),
    ((8, 2), (4, 1)),
    ((8, 1), (4, 2)),
)
TRANSLATION_WORDS = ("0123", "1032", "2301", "3210")


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def norm_matching(matching: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(tuple(sorted(pair)) for pair in matching))


def perm_axis_pair(pair: tuple[int, int], permutation: tuple[int, int, int, int]) -> tuple[int, int]:
    return tuple(sorted(AXES[permutation[AXES.index(axis)]] for axis in pair))  # type: ignore[return-value]


def perm_matching(
    matching: tuple[tuple[int, int], tuple[int, int]],
    permutation: tuple[int, int, int, int],
) -> tuple[tuple[int, int], ...]:
    return norm_matching((perm_axis_pair(matching[0], permutation), perm_axis_pair(matching[1], permutation)))


def value_bit_kernel() -> list[tuple[int, int, int, int]]:
    return [
        tuple(permutation)  # type: ignore[list-item]
        for permutation in itertools.permutations(range(4))
        if all(
            perm_matching(matching, tuple(permutation)) == norm_matching(matching)
            for matching in MATCHINGS
        )
    ]


def permute_label(label: int, permutation: tuple[int, int, int, int]) -> int:
    out = 0
    for old_index, axis in enumerate(AXES):
        if label & axis:
            out |= AXES[permutation[old_index]]
    return out


def cell_index(row: int, col: int) -> int:
    return (
        (((row >> 1) & 1) << 3)
        | ((row & 1) << 2)
        | (((col >> 1) & 1) << 1)
        | (col & 1)
    )


def word_indices(word: str) -> tuple[int, int, int, int]:
    return tuple(cell_index(row, int(word[row])) for row in range(4))  # type: ignore[return-value]


def plane_direction(labels: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    base = labels[0]
    return tuple(sorted(base ^ label for label in labels))  # type: ignore[return-value]


def selected_plane_key(labels: tuple[int, ...]) -> str:
    return ",".join(str(label + 1) for label in sorted(labels))


def build_kernel_v4_o5() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    terminal_records = [record for record in o2["records"] if record["endpoint"] == 24]
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]
    kernel = value_bit_kernel()

    selected_stabilizer_counter = Counter()
    selected_orbit_counter = Counter()
    terminal_image_plane_count_counter = Counter()
    terminal_image_direction_count_counter = Counter()
    terminal_image_direction_balanced_counter = Counter()
    terminal_image_direction_counter = Counter()
    terminal_intersection_pattern_counter = Counter()
    kernel_terminal_plane_intersection_counter = Counter()
    direct_equality_counter = Counter()
    terminal_set_full_translation_counter = Counter()

    sample_records = []

    for record in terminal_records:
        square = squares[record["square_index"]]
        profile = f2ext.cell_labeling_affine_profile([list(row) for row in square])
        offset = profile["offset_label"]
        columns = profile["linear_columns_as_labels"]

        def cell_value_label(index: int) -> int:
            out = offset
            for bit, column in zip(AXES, columns):
                if index & bit:
                    out ^= column
            return out

        selected_plane = tuple(sorted(value - 1 for value in record["selected_values"]))
        kernel_orbit = {
            tuple(sorted(permute_label(label, permutation) for label in selected_plane))
            for permutation in kernel
        }
        kernel_stabilizer = [
            permutation
            for permutation in kernel
            if tuple(sorted(permute_label(label, permutation) for label in selected_plane))
            == selected_plane
        ]

        terminal_image_planes = {
            tuple(
                sorted(cell_value_label(index) for index in word_indices(word))
            )
            for word in TRANSLATION_WORDS
        }
        terminal_image_directions = {
            plane_direction(plane) for plane in terminal_image_planes
        }
        terminal_image_directions_balanced = all(
            count_derivation.is_balanced_direction(direction)
            for direction in terminal_image_directions
        )
        intersection_pattern = tuple(
            sorted(len(set(plane) & set(selected_plane)) for plane in terminal_image_planes)
        )

        selected_stabilizer_counter[len(kernel_stabilizer)] += 1
        selected_orbit_counter[len(kernel_orbit)] += 1
        terminal_image_plane_count_counter[len(terminal_image_planes)] += 1
        terminal_image_direction_count_counter[len(terminal_image_directions)] += 1
        terminal_image_direction_balanced_counter[
            terminal_image_directions_balanced
        ] += 1
        for direction in terminal_image_directions:
            terminal_image_direction_counter[",".join(str(value) for value in direction)] += 1
        terminal_intersection_pattern_counter[intersection_pattern] += 1
        kernel_terminal_plane_intersection_counter[
            len(kernel_orbit & terminal_image_planes)
        ] += 1
        direct_equality_counter[kernel_orbit == terminal_image_planes] += 1
        terminal_set_full_translation_counter[
            record["terminal_set_is_full_translation_v4"]
        ] += 1

        if len(sample_records) < 5:
            sample_records.append(
                {
                    "square_index": record["square_index"],
                    "mask": record["mask"],
                    "selected_plane": selected_plane_key(selected_plane),
                    "kernel_orbit_size": len(kernel_orbit),
                    "kernel_stabilizer_size": len(kernel_stabilizer),
                    "terminal_image_plane_count": len(terminal_image_planes),
                    "terminal_image_direction_count": len(terminal_image_directions),
                    "terminal_image_directions_balanced": terminal_image_directions_balanced,
                    "terminal_image_directions": [
                        list(direction) for direction in sorted(terminal_image_directions)
                    ],
                    "terminal_plane_selected_intersections": list(intersection_pattern),
                    "kernel_orbit_intersection_with_terminal_planes": len(
                        kernel_orbit & terminal_image_planes
                    ),
                }
            )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O5",
            "description": "Audit of whether the value-bit kernel V4 coincides with the terminal translation V4.",
        },
        "terminal24_affine_record_count": len(terminal_records),
        "value_bit_kernel_size": len(kernel),
        "value_bit_kernel_permutations": [list(permutation) for permutation in kernel],
        "selected_plane_kernel_stabilizer_size_distribution": counter_json(
            selected_stabilizer_counter
        ),
        "selected_plane_kernel_orbit_size_distribution": counter_json(
            selected_orbit_counter
        ),
        "terminal_translation_image_plane_count_distribution": counter_json(
            terminal_image_plane_count_counter
        ),
        "terminal_translation_image_direction_count_distribution": counter_json(
            terminal_image_direction_count_counter
        ),
        "terminal_translation_image_direction_balanced_distribution": counter_json(
            terminal_image_direction_balanced_counter
        ),
        "terminal_translation_image_direction_distribution": counter_json(
            terminal_image_direction_counter
        ),
        "terminal_plane_selected_intersection_pattern_distribution": counter_json(
            terminal_intersection_pattern_counter
        ),
        "kernel_orbit_intersection_with_terminal_planes_distribution": counter_json(
            kernel_terminal_plane_intersection_counter
        ),
        "kernel_orbit_equals_terminal_translation_image_planes": counter_json(
            direct_equality_counter
        ),
        "terminal_set_full_translation_v4_distribution": counter_json(
            terminal_set_full_translation_counter
        ),
        "interpretation": {
            "direct_kernel_identification": "false",
            "reason": (
                "The value-bit kernel has size 4, but its orbit on the "
                "terminal selected value plane has size 2 and is disjoint from "
                "the four value planes obtained as images of the terminal "
                "translation diagonals."
            ),
            "positive_structure": (
                "For every exact-V4 affine record, the terminal translation "
                "diagonals map to the four cosets of one balanced value "
                "direction, and each such plane intersects the selected "
                "terminal value plane in exactly one point."
            ),
        },
        "sample_records": sample_records,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Kernel V4 Versus Terminal Translation V4",
        "",
        "Status: Phase O5 follow-up audit, intentionally outside the paper",
        "",
        "## Question",
        "",
        "Does the terminal translation `V4` coincide, through the global",
        "cell-value affine map, with the kernel of the value-bit action",
        "`S4 -> S3` on coordinate-axis matchings?",
        "",
        "## Verdict",
        "",
        "No: the direct identification is false in the certified exact-V4 affine",
        "class.",
        "",
        "## Evidence",
        "",
        f"- terminal affine records: `{result['terminal24_affine_record_count']}`",
        f"- value-bit kernel size: `{result['value_bit_kernel_size']}`",
        f"- selected-plane kernel stabilizer sizes: `{result['selected_plane_kernel_stabilizer_size_distribution']}`",
        f"- selected-plane kernel orbit sizes: `{result['selected_plane_kernel_orbit_size_distribution']}`",
        f"- kernel orbit equals terminal translation image planes: `{result['kernel_orbit_equals_terminal_translation_image_planes']}`",
        f"- kernel orbit intersection with terminal image planes: `{result['kernel_orbit_intersection_with_terminal_planes_distribution']}`",
        "",
        "Thus the value-bit kernel does not produce the terminal translation",
        "planes directly.",
        "",
        "## Positive Structure",
        "",
        f"- terminal translation image plane counts: `{result['terminal_translation_image_plane_count_distribution']}`",
        f"- terminal translation image direction counts: `{result['terminal_translation_image_direction_count_distribution']}`",
        f"- terminal translation image directions balanced: `{result['terminal_translation_image_direction_balanced_distribution']}`",
        f"- selected-plane intersection patterns: `{result['terminal_plane_selected_intersection_pattern_distribution']}`",
        "",
        "For every record, the terminal translation diagonals become four cosets",
        "of one balanced value direction, and each coset intersects the selected",
        "terminal plane in exactly one point.  This is the real structural",
        "relationship behind the terminal full-translation `V4`.",
        "",
        "## Guardrail",
        "",
        "Do not claim that the two `V4` objects coincide.  They live in related",
        "but different actions: value-bit symmetries on coordinate matchings",
        "versus permutation diagonals in the row/column domain.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_kernel_v4_o5()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "kernel_v4_o5.json"
        report_path = root / "results" / "KERNEL_V4_O5_REPORT.md"
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
