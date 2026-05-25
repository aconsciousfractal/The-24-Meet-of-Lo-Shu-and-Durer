"""Phase O5d audit: six-of-nine split for every selected value plane."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_affine_normal_count_derivation as count_derivation
import analyze_affine_normal_layer as affine_layer
import analyze_order4_f2_extension as f2ext
import analyze_six_of_nine_o5c as o5c
import analyze_terminal_parallel_torsor_o5b as torsor


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def direction_key(direction: tuple[int, ...]) -> str:
    return ",".join(str(value) for value in direction)


def selected_plane_key(values: list[int]) -> str:
    return ",".join(str(value) for value in sorted(values))


def selected_direction_key(record: dict) -> str:
    return direction_key(tuple(record["selected_direction"]))


def balanced_complement_data(
    selected_direction: tuple[int, int, int, int],
) -> dict:
    partner_direction = o5c.coordinate_partner(selected_direction)
    balanced_directions = [
        plane
        for plane in count_derivation.two_planes()
        if count_derivation.is_balanced_direction(plane)
    ]
    complements = [
        direction
        for direction in balanced_directions
        if count_derivation.span_rank(selected_direction, direction) == 4
    ]
    rank_counter = Counter()
    invertible = set()
    rank_one = set()
    for direction in complements:
        columns = o5c.graph_columns_relative_to_partner(
            selected_direction, partner_direction, direction
        )
        rank = o5c.graph_rank(columns)
        rank_counter[rank] += 1
        if rank == 2:
            invertible.add(direction)
        elif rank == 1:
            rank_one.add(direction)
    return {
        "partner_direction": partner_direction,
        "complements": set(complements),
        "invertible": invertible,
        "rank_one": rank_one,
        "rank_distribution": rank_counter,
    }


def build_selected_plane_six_of_nine_o5d() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    records = o2["records"]
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]

    by_plane: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_plane[selected_plane_key(record["selected_values"])].append(record)

    direction_cache: dict[tuple[int, int, int, int], dict] = {}
    plane_summaries = []
    violation_records = []
    plane_record_count_counter = Counter()
    used_direction_count_counter = Counter()
    used_direction_multiplicity_counter = Counter()
    plane_rank_split_counter = Counter()

    for plane_key, plane_records in sorted(by_plane.items()):
        selected_direction = tuple(plane_records[0]["selected_direction"])
        if selected_direction not in direction_cache:
            direction_cache[selected_direction] = balanced_complement_data(
                selected_direction
            )
        complement_data = direction_cache[selected_direction]
        used_direction_counter = Counter()

        for record in plane_records:
            profile = torsor.record_translation_torsor_profile(
                record, squares[record["square_index"]]
            )
            terminal_direction = profile["translation_direction"]
            used_direction_counter[terminal_direction] += 1
            if terminal_direction not in complement_data["invertible"]:
                violation_records.append(
                    {
                        "selected_plane": plane_key,
                        "square_index": record["square_index"],
                        "mask": record["mask"],
                        "terminal_direction": list(terminal_direction),
                    }
                )

        used_directions = set(used_direction_counter)
        unused_invertible = sorted(complement_data["invertible"] - used_directions)
        used_noninvertible = sorted(used_directions - complement_data["invertible"])
        rank_split = (
            len(complement_data["invertible"]),
            len(complement_data["rank_one"]),
        )
        plane_record_count_counter[len(plane_records)] += 1
        used_direction_count_counter[len(used_directions)] += 1
        used_direction_multiplicity_counter[
            tuple(sorted(used_direction_counter.values()))
        ] += 1
        plane_rank_split_counter[rank_split] += 1

        plane_summaries.append(
            {
                "selected_plane": plane_key,
                "selected_direction": list(selected_direction),
                "coordinate_partner_direction": list(
                    complement_data["partner_direction"]
                ),
                "record_count": len(plane_records),
                "balanced_complement_count": len(complement_data["complements"]),
                "balanced_complement_rank_distribution": counter_json(
                    complement_data["rank_distribution"]
                ),
                "invertible_graph_complement_count": len(complement_data["invertible"]),
                "rank_one_graph_complement_count": len(complement_data["rank_one"]),
                "used_terminal_direction_count": len(used_directions),
                "used_terminal_direction_distribution": counter_json(
                    Counter(
                        {
                            direction_key(direction): count
                            for direction, count in used_direction_counter.items()
                        }
                    )
                ),
                "used_directions_equal_invertible_complements": (
                    used_directions == complement_data["invertible"]
                ),
                "unused_invertible_complements": [
                    list(direction) for direction in unused_invertible
                ],
                "used_noninvertible_complements": [
                    list(direction) for direction in used_noninvertible
                ],
            }
        )

    by_selected_direction: dict[str, list[dict]] = defaultdict(list)
    for summary in plane_summaries:
        by_selected_direction[direction_key(tuple(summary["selected_direction"]))].append(
            summary
        )

    direction_summaries = []
    for direction, summaries in sorted(by_selected_direction.items()):
        direction_summaries.append(
            {
                "selected_direction": direction,
                "selected_plane_count": len(summaries),
                "all_planes_use_six_invertible_complements": all(
                    summary["used_directions_equal_invertible_complements"]
                    for summary in summaries
                ),
            }
        )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O5d",
            "description": "Shows the six-of-nine split for every selected value plane in the affine layer.",
        },
        "affine_square_mask_pair_count": len(records),
        "selected_plane_count": len(plane_summaries),
        "selected_direction_count": len(direction_summaries),
        "plane_record_count_distribution": counter_json(plane_record_count_counter),
        "used_direction_count_per_plane_distribution": counter_json(
            used_direction_count_counter
        ),
        "used_direction_multiplicity_per_plane_distribution": counter_json(
            used_direction_multiplicity_counter
        ),
        "balanced_complement_rank_split_distribution": counter_json(
            plane_rank_split_counter
        ),
        "all_planes_have_nine_balanced_complements": all(
            summary["balanced_complement_count"] == 9 for summary in plane_summaries
        ),
        "all_planes_have_six_invertible_and_three_rank_one_complements": all(
            summary["invertible_graph_complement_count"] == 6
            and summary["rank_one_graph_complement_count"] == 3
            for summary in plane_summaries
        ),
        "all_planes_use_exactly_invertible_complements": all(
            summary["used_directions_equal_invertible_complements"]
            for summary in plane_summaries
        ),
        "violation_count": len(violation_records),
        "violation_records": violation_records,
        "direction_summaries": direction_summaries,
        "plane_summaries": plane_summaries,
        "interpretation": {
            "general_six_of_nine": (
                "For every selected value plane in the globally affine layer, "
                "the nine balanced complements to its direction split as six "
                "invertible graphs plus three rank-one graphs relative to the "
                "coordinate partner direction."
            ),
            "used_directions": (
                "The terminal/translation directions used by the affine layer "
                "are exactly the six invertible graph complements, with each "
                "of the six occurring 24 times for each selected plane."
            ),
        },
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Six Of Nine For Every Selected Plane",
        "",
        "Status: Phase O5d follow-up audit, outside the paper",
        "",
        "## Question",
        "",
        "Does the O5c split",
        "",
        "```text",
        "9 balanced complements = 6 invertible graphs + 3 rank-one graphs",
        "```",
        "",
        "hold for every selected value plane in the globally affine layer,",
        "rather than only for `{11,12,15,16}`?",
        "",
        "## Answer",
        "",
        "Yes.  The split is uniform across all `24` selected value planes.",
        "",
        "Counters:",
        "",
        f"- affine square-mask pairs: `{result['affine_square_mask_pair_count']}`",
        f"- selected value planes: `{result['selected_plane_count']}`",
        f"- selected directions: `{result['selected_direction_count']}`",
        f"- plane record counts: `{result['plane_record_count_distribution']}`",
        f"- used direction counts per plane: `{result['used_direction_count_per_plane_distribution']}`",
        f"- used direction multiplicities per plane: `{result['used_direction_multiplicity_per_plane_distribution']}`",
        f"- balanced complement rank split: `{result['balanced_complement_rank_split_distribution']}`",
        f"- all planes use exactly invertible complements: `{result['all_planes_use_exactly_invertible_complements']}`",
        f"- violations: `{result['violation_count']}`",
        "",
        "Thus each selected plane has `144` affine square-mask records and uses",
        "six translation directions, each appearing `24` times.",
        "",
        "## Interpretation",
        "",
        "For each selected plane direction `U`, let `Q` be its coordinate",
        "partner in the matching.  The nine balanced complements to `U` are",
        "graphs of binary maps `Q -> U` with no zero rows.  The affine layer",
        "uses exactly the six invertible graphs.  This is the uniform version",
        "of the terminal-24 O5c result.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_selected_plane_six_of_nine_o5d()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "selected_plane_six_of_nine_o5d.json"
        report_path = root / "results" / "SELECTED_PLANE_SIX_OF_NINE_O5D_REPORT.md"
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
