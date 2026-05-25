"""Phase O5c audit explaining the terminal-24 six-of-nine direction split."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import analyze_affine_normal_count_derivation as count_derivation
import analyze_affine_normal_layer as affine_layer
import analyze_order4_f2_extension as f2ext
import analyze_terminal_parallel_torsor_o5b as torsor


VALUE_AXES = (8, 4, 2, 1)


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def direction_key(direction: tuple[int, ...]) -> str:
    return ",".join(str(value) for value in direction)


def coordinate_axes(direction: tuple[int, int, int, int]) -> tuple[int, int]:
    nonzero = sorted(value for value in direction if value != 0)
    for index, first in enumerate(nonzero):
        for second in nonzero[index + 1 :]:
            if first ^ second in nonzero:
                return tuple(sorted((first, second)))  # type: ignore[return-value]
    raise ValueError(f"not a coordinate direction: {direction}")


def coordinate_direction_from_axes(axes: tuple[int, int]) -> tuple[int, int, int, int]:
    first, second = axes
    return tuple(sorted((0, first, second, first ^ second)))  # type: ignore[return-value]


def coordinate_partner(direction: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    axes = set(coordinate_axes(direction))
    partner_axes = tuple(sorted(axis for axis in VALUE_AXES if axis not in axes))
    return coordinate_direction_from_axes(partner_axes)  # type: ignore[arg-type]


def graph_columns_relative_to_partner(
    selected_direction: tuple[int, int, int, int],
    partner_direction: tuple[int, int, int, int],
    direction: tuple[int, int, int, int],
) -> tuple[int, int]:
    """Write direction as graph of a map partner_direction -> selected_direction."""

    selected_axes = coordinate_axes(selected_direction)
    partner_axes = coordinate_axes(partner_direction)
    selected_mask = selected_axes[0] | selected_axes[1]
    partner_mask = partner_axes[0] | partner_axes[1]
    columns = []
    for axis in partner_axes:
        matches = [value for value in direction if value & partner_mask == axis]
        if len(matches) != 1:
            raise ValueError(
                f"direction {direction} is not a graph over partner {partner_direction}"
            )
        columns.append(matches[0] & selected_mask)
    return tuple(columns)  # type: ignore[return-value]


def graph_rank(columns: tuple[int, int]) -> int:
    return count_derivation.gf2_rank(columns)


def build_six_of_nine_o5c() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    terminal_records = [record for record in o2["records"] if record["endpoint"] == 24]
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]

    selected_direction = tuple(terminal_records[0]["selected_direction"])
    partner_direction = coordinate_partner(selected_direction)
    balanced_directions = [
        plane
        for plane in count_derivation.two_planes()
        if count_derivation.is_balanced_direction(plane)
    ]
    balanced_complements = [
        direction
        for direction in balanced_directions
        if count_derivation.span_rank(selected_direction, direction) == 4
    ]

    complement_details = []
    invertible_complements = set()
    rank_counter = Counter()
    complement_to_partner_counter = Counter()
    for direction in balanced_complements:
        columns = graph_columns_relative_to_partner(
            selected_direction, partner_direction, direction
        )
        rank = graph_rank(columns)
        complement_to_partner = (
            count_derivation.span_rank(partner_direction, direction) == 4
        )
        rank_counter[rank] += 1
        complement_to_partner_counter[complement_to_partner] += 1
        if rank == 2:
            invertible_complements.add(direction)
        complement_details.append(
            {
                "direction": list(direction),
                "graph_columns_partner_to_selected": list(columns),
                "graph_rank": rank,
                "complementary_to_partner_direction": complement_to_partner,
            }
        )

    terminal_direction_counter = Counter()
    terminal_direction_rank_counter = Counter()
    terminal_direction_partner_complement_counter = Counter()
    terminal_direction_in_invertible_counter = Counter()
    for record in terminal_records:
        profile = torsor.record_translation_torsor_profile(
            record, squares[record["square_index"]]
        )
        terminal_direction = profile["translation_direction"]
        columns = graph_columns_relative_to_partner(
            selected_direction, partner_direction, terminal_direction
        )
        rank = graph_rank(columns)
        terminal_direction_counter[direction_key(terminal_direction)] += 1
        terminal_direction_rank_counter[rank] += 1
        terminal_direction_partner_complement_counter[
            count_derivation.span_rank(partner_direction, terminal_direction) == 4
        ] += 1
        terminal_direction_in_invertible_counter[
            terminal_direction in invertible_complements
        ] += 1

    used_directions = {
        tuple(int(value) for value in key.split(","))
        for key in terminal_direction_counter
    }
    unused_balanced_complements = [
        direction for direction in balanced_complements if direction not in used_directions
    ]

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O5c",
            "description": "Explains the terminal-24 six-of-nine balanced-complement split.",
        },
        "terminal24_affine_record_count": len(terminal_records),
        "selected_direction": list(selected_direction),
        "coordinate_partner_direction": list(partner_direction),
        "balanced_complement_count": len(balanced_complements),
        "balanced_complement_graph_rank_distribution": counter_json(rank_counter),
        "balanced_complement_is_partner_complement_distribution": counter_json(
            complement_to_partner_counter
        ),
        "invertible_graph_complement_count": len(invertible_complements),
        "rank_one_balanced_complement_count": rank_counter[1],
        "terminal_direction_count": len(terminal_direction_counter),
        "terminal_direction_distribution": counter_json(terminal_direction_counter),
        "terminal_direction_graph_rank_distribution": counter_json(
            terminal_direction_rank_counter
        ),
        "terminal_direction_is_partner_complement_distribution": counter_json(
            terminal_direction_partner_complement_counter
        ),
        "terminal_direction_is_invertible_graph_distribution": counter_json(
            terminal_direction_in_invertible_counter
        ),
        "used_directions_equal_invertible_complements": used_directions
        == invertible_complements,
        "unused_balanced_complements": [list(direction) for direction in unused_balanced_complements],
        "balanced_complement_details": complement_details,
        "interpretation": {
            "six_of_nine_reason": (
                "Relative to the selected coordinate direction U and its "
                "matching partner Q, the nine balanced complements to U are "
                "graphs of the nine 2x2 binary maps Q -> U with no zero rows. "
                "The six terminal-24 directions are exactly the invertible "
                "maps, equivalently the complements to both U and Q."
            ),
            "excluded_three": (
                "The three unused balanced complements are rank-one graphs: "
                "they are transverse to U but intersect the partner direction Q."
            ),
        },
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Six Of Nine Balanced Complements",
        "",
        "Status: Phase O5c follow-up audit, outside the paper",
        "",
        "## Question",
        "",
        "In the terminal-24 exact-`V4` affine class, why do the terminal",
        "directions use six of the nine balanced complements to the selected",
        "plane direction?",
        "",
        "## Answer",
        "",
        "Let `U` be the selected terminal value-plane direction and `Q` its",
        "coordinate partner in the matching:",
        "",
        f"- `U = {result['selected_direction']}`",
        f"- `Q = {result['coordinate_partner_direction']}`",
        "",
        "Every balanced complement `W` to `U` is a graph of a binary linear",
        "map:",
        "",
        "```text",
        "Q -> U",
        "```",
        "",
        "The nine balanced complements are exactly the maps with no zero rows.",
        "The six terminal-24 directions are exactly the invertible maps.",
        "",
        "Counters:",
        "",
        f"- balanced complements to `U`: `{result['balanced_complement_count']}`",
        f"- graph-rank distribution: `{result['balanced_complement_graph_rank_distribution']}`",
        f"- complements also transverse to `Q`: `{result['balanced_complement_is_partner_complement_distribution']}`",
        f"- terminal directions: `{result['terminal_direction_count']}`",
        f"- terminal direction distribution: `{result['terminal_direction_distribution']}`",
        f"- terminal graph-rank distribution: `{result['terminal_direction_graph_rank_distribution']}`",
        f"- terminal directions equal invertible complements: `{result['used_directions_equal_invertible_complements']}`",
        "",
        "## Interpretation",
        "",
        "The six-of-nine split is therefore not accidental:",
        "",
        "```text",
        "9 balanced complements = 6 invertible graphs + 3 rank-one graphs",
        "terminal-24 exact-V4 uses the 6 invertible graphs",
        "```",
        "",
        "Equivalently, the terminal directions are the balanced directions",
        "complementary to both directions in the selected coordinate-axis",
        "matching.  The three excluded directions are still transverse to the",
        "selected plane, but they meet the partner direction nontrivially.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_six_of_nine_o5c()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "six_of_nine_o5c.json"
        report_path = root / "results" / "SIX_OF_NINE_O5C_REPORT.md"
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
