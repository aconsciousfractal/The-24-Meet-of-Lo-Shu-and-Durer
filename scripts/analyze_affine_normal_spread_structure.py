"""Phase O3 spread audit for the affine normal order-4 layer."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import analyze_affine_normal_layer as affine_layer
import analyze_order4_f2_extension as f2ext
import enumerate_order4_endpoints as order4


VALUE_AXES = (8, 4, 2, 1)


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def plane_key(values: list[int]) -> str:
    return ",".join(str(value) for value in sorted(values))


def direction_key(direction: list[int] | tuple[int, ...]) -> str:
    return ",".join(str(value) for value in direction)


def direction_axes(direction: str) -> tuple[int, int]:
    labels = [int(value) for value in direction.split(",")]
    axes = sorted(value for value in labels if value != 0)
    if len(axes) != 3:
        raise ValueError(f"unexpected direction {direction}")
    # A coordinate 2-plane direction has labels {0,a,b,a^b}; the axes are
    # the two labels whose xor is the third.
    for i, a in enumerate(axes):
        for b in axes[i + 1 :]:
            if (a ^ b) in axes:
                return tuple(sorted((a, b)))  # type: ignore[return-value]
    raise ValueError(f"not a coordinate 2-plane direction {direction}")


def matching_key(directions: tuple[str, str]) -> str:
    axis_pairs = sorted(direction_axes(direction) for direction in directions)
    return " | ".join(",".join(str(value) for value in pair) for pair in axis_pairs)


def permute_label_bits(label: int, permutation: tuple[int, int, int, int]) -> int:
    out = 0
    for old_index, axis in enumerate(VALUE_AXES):
        if label & axis:
            out |= VALUE_AXES[permutation[old_index]]
    return out


def relabel_square_by_value_bit_permutation(
    square: tuple[tuple[int, ...], ...],
    permutation: tuple[int, int, int, int],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(permute_label_bits(value - 1, permutation) + 1 for value in row)
        for row in square
    )


def matching_action_profile(
    square_summaries: list[dict],
) -> dict:
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]
    index_by_square = {square: index for index, square in enumerate(squares)}
    matching_by_index = {
        summary["square_index"]: summary["coordinate_axis_matching"]
        for summary in square_summaries
    }
    affine_indices = set(matching_by_index)
    matchings = sorted(set(matching_by_index.values()))

    induced_actions = Counter()
    preserving_permutations = []
    matching_stabilizers = Counter()

    for permutation in itertools.permutations(range(4)):
        image_by_matching: dict[str, set[str]] = {matching: set() for matching in matchings}
        preserves_layer = True
        for square_index in affine_indices:
            relabeled = relabel_square_by_value_bit_permutation(
                squares[square_index], permutation
            )
            if not order4.is_magic(relabeled):
                preserves_layer = False
                break
            canonical = order4.canonical_square(relabeled)
            image_index = index_by_square.get(canonical)
            if image_index not in affine_indices:
                preserves_layer = False
                break
            image_by_matching[matching_by_index[square_index]].add(
                matching_by_index[image_index]
            )
        if not preserves_layer:
            continue
        induced = []
        for matching in matchings:
            images = image_by_matching[matching]
            if len(images) != 1:
                preserves_layer = False
                break
            induced.append(next(iter(images)))
        if not preserves_layer:
            continue
        induced_key = " ; ".join(
            f"{source}->{target}" for source, target in zip(matchings, induced)
        )
        induced_actions[induced_key] += 1
        preserving_permutations.append(
            {
                "value_bit_permutation": list(permutation),
                "induced_matching_action": induced_key,
            }
        )
        for source, target in zip(matchings, induced):
            if source == target:
                matching_stabilizers[source] += 1

    return {
        "value_bit_permutation_count": len(list(itertools.permutations(range(4)))),
        "affine_layer_preserving_value_bit_permutations": len(
            preserving_permutations
        ),
        "all_value_bit_permutations_preserve_affine_layer": (
            len(preserving_permutations) == 24
        ),
        "induced_matching_action_count": len(induced_actions),
        "induced_matching_action_preimage_distribution": counter_json(
            Counter(induced_actions.values())
        ),
        "matching_stabilizer_sizes": counter_json(matching_stabilizers),
        "preserving_permutations": preserving_permutations,
    }


def build_affine_normal_spread_structure() -> dict:
    o2 = affine_layer.build_affine_normal_layer()

    by_square: dict[int, list[dict]] = defaultdict(list)
    for record in o2["records"]:
        by_square[record["square_index"]].append(record)

    square_summaries = []
    matching_counter = Counter()
    plane_set_counter = Counter()
    matching_plane_counter: dict[str, Counter] = defaultdict(Counter)
    matching_endpoint_counter: dict[str, Counter] = defaultdict(Counter)

    for square_index, records in sorted(by_square.items()):
        planes = tuple(sorted(plane_key(record["selected_values"]) for record in records))
        directions = tuple(
            sorted({direction_key(record["selected_direction"]) for record in records})
        )
        matching = matching_key(directions)  # type: ignore[arg-type]
        matching_counter[matching] += 1
        plane_set_counter[planes] += 1
        for record in records:
            matching_plane_counter[matching][plane_key(record["selected_values"])] += 1
            matching_endpoint_counter[matching][record["endpoint"]] += 1
        square_summaries.append(
            {
                "square_index": square_index,
                "selected_plane_count": len(set(planes)),
                "selected_direction_count": len(directions),
                "selected_planes": list(planes),
                "selected_directions": list(directions),
                "coordinate_axis_matching": matching,
            }
        )

    matching_summaries = []
    for matching in sorted(matching_counter):
        plane_counts = matching_plane_counter[matching]
        endpoint_counts = matching_endpoint_counter[matching]
        matching_summaries.append(
            {
                "coordinate_axis_matching": matching,
                "square_count": matching_counter[matching],
                "selected_plane_count": len(plane_counts),
                "selected_plane_count_distribution": counter_json(
                    Counter(plane_counts.values())
                ),
                "selected_planes": [
                    {"selected_values": plane, "pair_count": plane_counts[plane]}
                    for plane in sorted(plane_counts)
                ],
                "endpoint_distribution": counter_json(endpoint_counts),
            }
        )

    action_profile = matching_action_profile(square_summaries)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O3",
            "description": "Spread/matching structure behind the affine normal order-4 24 x 144 split.",
        },
        "affine_square_count": o2["affine_square_count"],
        "affine_square_mask_pair_count": o2["affine_square_mask_pair_count"],
        "selected_value_plane_count": o2["selected_value_plane_count"],
        "selected_value_plane_count_distribution": o2[
            "selected_value_plane_count_distribution"
        ],
        "square_selected_plane_count_distribution": counter_json(
            Counter(summary["selected_plane_count"] for summary in square_summaries)
        ),
        "square_selected_direction_count_distribution": counter_json(
            Counter(summary["selected_direction_count"] for summary in square_summaries)
        ),
        "coordinate_axis_matching_count": len(matching_counter),
        "coordinate_axis_matching_distribution": counter_json(matching_counter),
        "plane_set_count": len(plane_set_counter),
        "plane_set_count_distribution": counter_json(Counter(plane_set_counter.values())),
        "all_squares_have_eight_planes_and_two_directions": all(
            summary["selected_plane_count"] == 8
            and summary["selected_direction_count"] == 2
            for summary in square_summaries
        ),
        "all_matchings_have_144_squares": set(matching_counter.values()) == {144},
        "all_matching_planes_have_144_pairs": all(
            set(counter.values()) == {144}
            for counter in matching_plane_counter.values()
        ),
        "value_bit_matching_action": action_profile,
        "matching_summaries": matching_summaries,
        "square_summaries": square_summaries,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Affine Normal Spread Structure Audit",
        "",
        "Status: Phase O3 spread/matching explanation",
        "",
        "## Purpose",
        "",
        "Phase O2 found the finite uniformity",
        "",
        "```text",
        "3456 = 24 selected value planes x 144 pairs.",
        "```",
        "",
        "This audit explains the first structural layer behind that uniformity.",
        "",
        "## Square-Level Structure",
        "",
        f"- globally affine representatives: `{result['affine_square_count']}`",
        f"- affine square-mask pairs: `{result['affine_square_mask_pair_count']}`",
        f"- selected value planes: `{result['selected_value_plane_count']}`",
        f"- per-square selected plane counts: `{result['square_selected_plane_count_distribution']}`",
        f"- per-square selected direction counts: `{result['square_selected_direction_count_distribution']}`",
        "",
        "Each globally affine representative sends the eight admissible masks to",
        "exactly eight selected value planes: all four cosets of one coordinate",
        "2-plane direction and all four cosets of a complementary coordinate",
        "2-plane direction.",
        "",
        "## Coordinate-Axis Matchings",
        "",
        f"- matchings: `{result['coordinate_axis_matching_count']}`",
        f"- matching distribution: `{result['coordinate_axis_matching_distribution']}`",
        f"- plane-set count distribution: `{result['plane_set_count_distribution']}`",
        "",
        "The three matchings are the three partitions of the four coordinate axes",
        "into two unordered pairs.",
        "",
        "## Value-Bit Symmetry",
        "",
        f"- value-bit permutations tested: `{result['value_bit_matching_action']['value_bit_permutation_count']}`",
        f"- preserving the affine normal layer: `{result['value_bit_matching_action']['affine_layer_preserving_value_bit_permutations']}`",
        f"- induced matching actions: `{result['value_bit_matching_action']['induced_matching_action_count']}`",
        f"- action preimage distribution: `{result['value_bit_matching_action']['induced_matching_action_preimage_distribution']}`",
        f"- matching stabilizer sizes: `{result['value_bit_matching_action']['matching_stabilizer_sizes']}`",
        "",
        "All `24` permutations of the four value bits preserve the globally",
        "affine normal layer.  Their induced action on the three coordinate-axis",
        "matchings has `6` actions, each with `4` preimages.  Equivalently, this",
        "is the natural `S4 -> S3` action on the three perfect matchings of four",
        "axes.  Each matching has stabilizer size `8`, hence the three matching",
        "classes have equal size.",
        "",
        "## Matching Details",
        "",
    ]
    for summary in result["matching_summaries"]:
        lines.extend(
            [
                f"### `{summary['coordinate_axis_matching']}`",
                "",
                f"- square count: `{summary['square_count']}`",
                f"- selected planes: `{summary['selected_plane_count']}`",
                f"- selected plane count distribution: `{summary['selected_plane_count_distribution']}`",
                f"- endpoint distribution: `{summary['endpoint_distribution']}`",
                "",
            ]
        )
        for row in summary["selected_planes"]:
            lines.append(
                f"- `{row['selected_values']}`: `{row['pair_count']}`"
            )
        lines.append("")
    lines.extend(
        [
            "## Interpretation",
            "",
            "The number `144` is explained at the first structural level by two",
            "nested facts:",
            "",
            "```text",
            "432 affine representatives = 3 coordinate-axis matchings x 144",
            "each affine representative contributes 8 planes = 2 directions x 4 cosets",
            "therefore 3456 affine pairs = 24 planes x 144 pairs",
            "```",
            "",
            "The terminal-24 exact-V4 class is the high selected value plane",
            "`{11,12,15,16}` inside one of these three matchings.",
            "",
            "## Remaining Conceptual Gap",
            "",
            "The group action explains the equality of the three matching classes.",
            "The remaining proof target is narrower: derive the total `432` count",
            "of globally affine essential representatives without enumerating the",
            "full order-4 normal-square atlas.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_affine_normal_spread_structure()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "affine_normal_spread_structure.json"
        report_path = root / "results" / "AFFINE_NORMAL_SPREAD_STRUCTURE_REPORT.md"
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
