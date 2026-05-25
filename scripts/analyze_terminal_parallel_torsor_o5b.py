"""Phase O5b audit of the terminal V4 parallel-class torsor."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import analyze_affine_normal_count_derivation as count_derivation
import analyze_affine_normal_layer as affine_layer
import analyze_kernel_v4_o5 as o5
import analyze_order4_f2_extension as f2ext


TRANSLATION_WORDS_BY_LABEL = {
    0: "0123",
    1: "1032",
    2: "2301",
    3: "3210",
}


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def selected_plane_key(labels: tuple[int, ...]) -> str:
    return ",".join(str(label + 1) for label in sorted(labels))


def affine_point_map_is_linear_over_base(point_map: dict[int, int]) -> bool:
    base = point_map[0]
    return point_map[3] == (base ^ (point_map[1] ^ base) ^ (point_map[2] ^ base))


def point_orbit_sizes(points: tuple[int, ...], permutations: list[tuple[int, int, int, int]]) -> tuple[int, ...]:
    unused = set(points)
    orbits = []
    while unused:
        seed = min(unused)
        orbit = {o5.permute_label(seed, permutation) for permutation in permutations}
        orbits.append(len(orbit))
        unused -= orbit
    return tuple(sorted(orbits))


def record_translation_torsor_profile(record: dict, square: tuple[tuple[int, ...], ...]) -> dict:
    profile = f2ext.cell_labeling_affine_profile([list(row) for row in square])
    offset = profile["offset_label"]
    columns = profile["linear_columns_as_labels"]

    def cell_value_label(index: int) -> int:
        out = offset
        for bit, column in zip(o5.AXES, columns):
            if index & bit:
                out ^= column
        return out

    selected_plane = tuple(sorted(value - 1 for value in record["selected_values"]))
    selected_direction = o5.plane_direction(selected_plane)
    translation_planes_by_label = {
        label: tuple(
            sorted(cell_value_label(index) for index in o5.word_indices(word))
        )
        for label, word in TRANSLATION_WORDS_BY_LABEL.items()
    }
    translation_directions = {
        o5.plane_direction(plane) for plane in translation_planes_by_label.values()
    }
    assert len(translation_directions) == 1
    translation_direction = next(iter(translation_directions))
    intersections = {
        label: tuple(sorted(set(plane) & set(selected_plane)))
        for label, plane in translation_planes_by_label.items()
    }
    point_map = {
        label: points[0]
        for label, points in intersections.items()
        if len(points) == 1
    }
    return {
        "selected_plane": selected_plane,
        "selected_direction": selected_direction,
        "translation_planes_by_label": translation_planes_by_label,
        "translation_direction": translation_direction,
        "intersections": intersections,
        "point_map": point_map,
    }


def summarize_translation_torsor(records: list[dict], squares: list[tuple[tuple[int, ...], ...]]) -> dict:
    direction_balanced_counter = Counter()
    complementary_counter = Counter()
    transversal_counter = Counter()
    bijection_counter = Counter()
    affine_counter = Counter()

    for record in records:
        profile = record_translation_torsor_profile(record, squares[record["square_index"]])
        selected_direction = profile["selected_direction"]
        translation_direction = profile["translation_direction"]
        point_map = profile["point_map"]

        direction_balanced_counter[
            count_derivation.is_balanced_direction(translation_direction)
        ] += 1
        complementary_counter[
            count_derivation.span_rank(selected_direction, translation_direction) == 4
        ] += 1
        transversal_counter[
            tuple(sorted(len(points) for points in profile["intersections"].values()))
        ] += 1
        bijection_counter[
            len(point_map) == 4
            and set(point_map.values()) == set(profile["selected_plane"])
        ] += 1
        affine_counter[affine_point_map_is_linear_over_base(point_map)] += 1

    return {
        "record_count": len(records),
        "translation_direction_balanced_distribution": counter_json(
            direction_balanced_counter
        ),
        "translation_direction_complementary_to_selected_distribution": counter_json(
            complementary_counter
        ),
        "translation_transversal_intersection_distribution": counter_json(
            transversal_counter
        ),
        "translation_to_selected_point_map_bijection_distribution": counter_json(
            bijection_counter
        ),
        "translation_to_selected_point_map_affine_distribution": counter_json(
            affine_counter
        ),
    }


def build_terminal_parallel_torsor_o5b() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    all_affine_records = o2["records"]
    full_translation_records = [
        record
        for record in all_affine_records
        if record["terminal_set_is_full_translation_v4"]
    ]
    terminal_records = [record for record in o2["records"] if record["endpoint"] == 24]
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]

    all_balanced = [
        plane
        for plane in count_derivation.two_planes()
        if count_derivation.is_balanced_direction(plane)
    ]
    value_bit_kernel = o5.value_bit_kernel()

    selected_direction_counter = Counter()
    terminal_direction_counter = Counter()
    terminal_direction_balanced_counter = Counter()
    terminal_direction_complementary_counter = Counter()
    selected_plane_transversal_counter = Counter()
    point_map_bijection_counter = Counter()
    point_map_affine_counter = Counter()
    point_map_direction_counter = Counter()
    balanced_complements_count_counter = Counter()
    terminal_direction_is_selected_complement_counter = Counter()
    kernel_setwise_stabilizer_size_counter = Counter()
    kernel_setwise_point_orbit_counter = Counter()
    kernel_full_orbit_size_counter = Counter()

    sample_records = []

    for record in terminal_records:
        profile = record_translation_torsor_profile(
            record, squares[record["square_index"]]
        )
        selected_plane = profile["selected_plane"]
        selected_direction = profile["selected_direction"]
        terminal_direction = profile["translation_direction"]
        intersections = profile["intersections"]
        point_map = profile["point_map"]

        selected_complements = [
            direction
            for direction in all_balanced
            if count_derivation.span_rank(selected_direction, direction) == 4
        ]
        kernel_setwise_stabilizer = [
            permutation
            for permutation in value_bit_kernel
            if tuple(
                sorted(o5.permute_label(label, permutation) for label in selected_plane)
            )
            == selected_plane
        ]
        kernel_full_plane_orbit = {
            tuple(sorted(o5.permute_label(label, permutation) for label in selected_plane))
            for permutation in value_bit_kernel
        }

        selected_direction_counter[",".join(str(value) for value in selected_direction)] += 1
        terminal_direction_counter[",".join(str(value) for value in terminal_direction)] += 1
        terminal_direction_balanced_counter[
            count_derivation.is_balanced_direction(terminal_direction)
        ] += 1
        terminal_direction_complementary_counter[
            count_derivation.span_rank(selected_direction, terminal_direction) == 4
        ] += 1
        selected_plane_transversal_counter[
            tuple(sorted(len(points) for points in intersections.values()))
        ] += 1
        point_map_bijection_counter[
            len(point_map) == 4 and set(point_map.values()) == set(selected_plane)
        ] += 1
        point_map_affine_counter[affine_point_map_is_linear_over_base(point_map)] += 1
        point_map_direction_counter[
            o5.plane_direction(tuple(point_map[label] for label in sorted(point_map)))
            == selected_direction
        ] += 1
        balanced_complements_count_counter[len(selected_complements)] += 1
        terminal_direction_is_selected_complement_counter[
            terminal_direction in selected_complements
        ] += 1
        kernel_setwise_stabilizer_size_counter[len(kernel_setwise_stabilizer)] += 1
        kernel_setwise_point_orbit_counter[
            point_orbit_sizes(selected_plane, kernel_setwise_stabilizer)
        ] += 1
        kernel_full_orbit_size_counter[len(kernel_full_plane_orbit)] += 1

        if len(sample_records) < 5:
            sample_records.append(
                {
                    "square_index": record["square_index"],
                    "mask": record["mask"],
                    "selected_plane": selected_plane_key(selected_plane),
                    "selected_direction": list(selected_direction),
                    "terminal_direction": list(terminal_direction),
                    "terminal_direction_balanced": count_derivation.is_balanced_direction(
                        terminal_direction
                    ),
                    "selected_direction_complementary_to_terminal_direction": (
                        count_derivation.span_rank(selected_direction, terminal_direction)
                        == 4
                    ),
                    "terminal_coset_intersections": {
                        str(label): list(points)
                        for label, points in sorted(intersections.items())
                    },
                    "point_map_value_labels": {
                        str(label): point + 1 for label, point in sorted(point_map.items())
                    },
                    "point_map_affine": affine_point_map_is_linear_over_base(point_map),
                    "kernel_setwise_stabilizer_size": len(kernel_setwise_stabilizer),
                    "kernel_setwise_point_orbit_sizes": list(
                        point_orbit_sizes(selected_plane, kernel_setwise_stabilizer)
                    ),
                    "kernel_full_plane_orbit_size": len(kernel_full_plane_orbit),
                }
            )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O5b",
            "description": "Terminal translation V4 as a parallel-class torsor over the selected value plane.",
        },
        "all_affine_translation_torsor_summary": summarize_translation_torsor(
            all_affine_records, squares
        ),
        "full_translation_terminal_torsor_summary": summarize_translation_torsor(
            full_translation_records, squares
        ),
        "terminal24_affine_record_count": len(terminal_records),
        "selected_direction_distribution": counter_json(selected_direction_counter),
        "terminal_direction_distribution": counter_json(terminal_direction_counter),
        "terminal_direction_balanced_distribution": counter_json(
            terminal_direction_balanced_counter
        ),
        "terminal_direction_complementary_to_selected_distribution": counter_json(
            terminal_direction_complementary_counter
        ),
        "selected_plane_transversal_intersection_distribution": counter_json(
            selected_plane_transversal_counter
        ),
        "terminal_to_selected_point_map_bijection_distribution": counter_json(
            point_map_bijection_counter
        ),
        "terminal_to_selected_point_map_affine_distribution": counter_json(
            point_map_affine_counter
        ),
        "terminal_to_selected_point_map_direction_distribution": counter_json(
            point_map_direction_counter
        ),
        "balanced_complements_to_selected_direction_count_distribution": counter_json(
            balanced_complements_count_counter
        ),
        "terminal_direction_is_balanced_complement_distribution": counter_json(
            terminal_direction_is_selected_complement_counter
        ),
        "kernel_setwise_stabilizer_size_distribution": counter_json(
            kernel_setwise_stabilizer_size_counter
        ),
        "kernel_setwise_point_orbit_size_distribution": counter_json(
            kernel_setwise_point_orbit_counter
        ),
        "kernel_full_selected_plane_orbit_size_distribution": counter_json(
            kernel_full_orbit_size_counter
        ),
        "interpretation": {
            "terminal_torsor_statement": (
                "Across the full affine square-mask layer, the fixed domain "
                "translation V4 maps affinely and bijectively to the selected "
                "value plane by intersecting its four parallel value-space "
                "cosets with that plane.  In the full-translation terminal "
                "subclass, this is the terminal V4."
            ),
            "transversal_reason": (
                "The selected plane direction is complementary to the terminal "
                "balanced direction, so the selected plane is a section of the "
                "quotient by that direction."
            ),
            "kernel_guardrail": (
                "The value-bit kernel V4 does not act transitively on the "
                "selected plane; only a size-2 setwise stabilizer remains, with "
                "point-orbit pattern (1,1,2)."
            ),
        },
        "sample_records": sample_records,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Terminal Parallel-Class Torsor",
        "",
        "Status: Phase O5b follow-up audit, outside the paper",
        "",
        "## Question",
        "",
        "After Phase O5 ruled out direct equality of the two `V4` objects,",
        "does the terminal translation `V4` still define a torsor over the",
        "selected terminal value plane?",
        "",
        "## Certified Answer",
        "",
        "Yes, and the statement is broader than terminal-24.  Across the",
        "full globally affine square-mask layer, the four fixed translation",
        "diagonals map to four cosets of one balanced value direction.  The",
        "selected value plane is a transversal to those cosets.  In the",
        "full-translation terminal subclass, this fixed translation `V4` is",
        "the terminal `V4`.",
        "",
        "Full affine-layer counters:",
        "",
        f"- all affine square-mask records: `{result['all_affine_translation_torsor_summary']['record_count']}`",
        f"- translation directions balanced: `{result['all_affine_translation_torsor_summary']['translation_direction_balanced_distribution']}`",
        f"- translation direction complementary to selected direction: `{result['all_affine_translation_torsor_summary']['translation_direction_complementary_to_selected_distribution']}`",
        f"- transversal intersection patterns: `{result['all_affine_translation_torsor_summary']['translation_transversal_intersection_distribution']}`",
        f"- translation-to-selected point map affine: `{result['all_affine_translation_torsor_summary']['translation_to_selected_point_map_affine_distribution']}`",
        "",
        "Full-translation terminal-subclass counters:",
        "",
        f"- full-translation records: `{result['full_translation_terminal_torsor_summary']['record_count']}`",
        f"- terminal torsor affine maps: `{result['full_translation_terminal_torsor_summary']['translation_to_selected_point_map_affine_distribution']}`",
        "",
        "Terminal-24 exact-`V4` counters:",
        "",
        f"- selected direction distribution: `{result['selected_direction_distribution']}`",
        f"- terminal direction distribution: `{result['terminal_direction_distribution']}`",
        f"- terminal directions balanced: `{result['terminal_direction_balanced_distribution']}`",
        f"- terminal direction complementary to selected direction: `{result['terminal_direction_complementary_to_selected_distribution']}`",
        f"- transversal intersection patterns: `{result['selected_plane_transversal_intersection_distribution']}`",
        f"- terminal-to-selected point map bijective: `{result['terminal_to_selected_point_map_bijection_distribution']}`",
        f"- terminal-to-selected point map affine: `{result['terminal_to_selected_point_map_affine_distribution']}`",
        "",
        "Thus the map",
        "",
        "```text",
        "terminal translation label -> unique point of P in the corresponding W-coset",
        "```",
        "",
        "is an affine bijection for every terminal-24 exact-`V4` record, and",
        "the same fixed-translation torsor statement holds for all `3456`",
        "globally affine square-mask pairs.",
        "",
        "## Kernel Guardrail",
        "",
        "The value-bit kernel is still not the terminal translation group:",
        "",
        f"- kernel setwise stabilizer sizes: `{result['kernel_setwise_stabilizer_size_distribution']}`",
        f"- kernel setwise point-orbit sizes on P: `{result['kernel_setwise_point_orbit_size_distribution']}`",
        f"- full kernel orbit size on selected planes: `{result['kernel_full_selected_plane_orbit_size_distribution']}`",
        "",
        "Only a size-2 subgroup of the value-bit kernel stabilizes the selected",
        "plane, and its point-orbit pattern is `(1,1,2)`, not a transitive",
        "`V4` action on the four points.",
        "",
        "## Interpretation",
        "",
        "The correct structure is a quotient-section relation in `F2^4`: the",
        "selected value plane is a section for the quotient by the balanced",
        "translation-image direction.  When the terminal set is the full",
        "translation subgroup, the terminal translation `V4` is identified",
        "with the four quotient cosets through this section.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_terminal_parallel_torsor_o5b()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "terminal_parallel_torsor_o5b.json"
        report_path = root / "results" / "TERMINAL_PARALLEL_TORSOR_O5B_REPORT.md"
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
