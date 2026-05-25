"""Phase O5e/O5f audit of the final 24-factor in the affine torsor layer."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_affine_normal_layer as affine_layer
import analyze_order4_f2_extension as f2ext
import analyze_terminal_parallel_torsor_o5b as torsor


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def direction_of_plane(plane: tuple[int, ...]) -> tuple[int, int, int, int]:
    base = plane[0]
    return tuple(sorted(base ^ point for point in plane))  # type: ignore[return-value]


def affine_maps_to_plane(plane: tuple[int, ...]) -> set[tuple[int, int, int, int]]:
    """All affine bijections from the fixed 4-point translation plane to plane."""

    direction = [value for value in direction_of_plane(plane) if value != 0]
    maps = set()
    for base in plane:
        for first in direction:
            for second in direction:
                if first == second:
                    continue
                maps.add((base, base ^ first, base ^ second, base ^ first ^ second))
    return maps


def point_map_key(profile: dict) -> tuple[int, int, int, int]:
    return tuple(profile["point_map"][label] for label in (0, 1, 2, 3))  # type: ignore[return-value]


def plane_key(plane: tuple[int, ...]) -> str:
    return ",".join(str(value + 1) for value in plane)


def direction_key(direction: tuple[int, ...]) -> str:
    return ",".join(str(value) for value in direction)


def map_key(mapping: tuple[int, int, int, int]) -> str:
    return ",".join(str(value + 1) for value in mapping)


def build_torsor_parametrization_o5e_o5f() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    records = o2["records"]
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]

    fibers: dict[tuple[tuple[int, ...], tuple[int, ...]], list[dict]] = defaultdict(list)
    for record in records:
        profile = torsor.record_translation_torsor_profile(
            record, squares[record["square_index"]]
        )
        selected_plane = tuple(sorted(profile["selected_plane"]))
        translation_direction = tuple(profile["translation_direction"])
        fibers[(selected_plane, translation_direction)].append(
            {
                "square_index": record["square_index"],
                "mask": record["mask"],
                "endpoint": record["endpoint"],
                "terminal_set_is_full_translation_v4": record[
                    "terminal_set_is_full_translation_v4"
                ],
                "point_map": point_map_key(profile),
            }
        )

    fiber_size_counter = Counter()
    distinct_point_map_counter = Counter()
    point_map_multiplicity_pattern_counter = Counter()
    point_map_mask_pair_counter = Counter()
    agl_torsor_counter = Counter()
    full_affine_map_count_counter = Counter()
    endpoint_counter_by_agl_status: dict[bool, Counter] = {
        True: Counter(),
        False: Counter(),
    }
    sample_failures = []
    sample_successes = []
    global_refined_keys = set()

    for (selected_plane, translation_direction), fiber_records in sorted(
        fibers.items(),
        key=lambda item: (plane_key(item[0][0]), direction_key(item[0][1])),
    ):
        point_map_counts = Counter(record["point_map"] for record in fiber_records)
        point_mask_pairs = {
            (record["point_map"], record["mask"]) for record in fiber_records
        }
        all_affine_maps = affine_maps_to_plane(selected_plane)
        realized_maps = set(point_map_counts)
        realizes_all_affine_maps = realized_maps == all_affine_maps

        fiber_size_counter[len(fiber_records)] += 1
        distinct_point_map_counter[len(realized_maps)] += 1
        point_map_multiplicity_pattern_counter[
            tuple(sorted(point_map_counts.values(), reverse=True))
        ] += 1
        point_map_mask_pair_counter[len(point_mask_pairs)] += 1
        agl_torsor_counter[realizes_all_affine_maps] += 1
        full_affine_map_count_counter[len(all_affine_maps)] += 1
        for record in fiber_records:
            endpoint_counter_by_agl_status[realizes_all_affine_maps][
                record["endpoint"]
            ] += 1
            global_refined_keys.add(
                (
                    selected_plane,
                    translation_direction,
                    record["point_map"],
                    record["mask"],
                )
            )

        sample = {
            "selected_plane": plane_key(selected_plane),
            "translation_direction": direction_key(translation_direction),
            "fiber_size": len(fiber_records),
            "all_affine_map_count": len(all_affine_maps),
            "distinct_point_map_count": len(realized_maps),
            "point_map_multiplicity_pattern": list(
                sorted(point_map_counts.values(), reverse=True)
            ),
            "point_map_mask_pair_count": len(point_mask_pairs),
            "realizes_all_affine_maps": realizes_all_affine_maps,
        }
        if realizes_all_affine_maps and len(sample_successes) < 3:
            sample_successes.append(sample)
        if not realizes_all_affine_maps and len(sample_failures) < 5:
            duplicate_maps = [
                {
                    "point_map": map_key(mapping),
                    "multiplicity": count,
                    "records": [
                        {
                            "square_index": record["square_index"],
                            "mask": record["mask"],
                            "endpoint": record["endpoint"],
                        }
                        for record in fiber_records
                        if record["point_map"] == mapping
                    ],
                }
                for mapping, count in point_map_counts.items()
                if count > 1
            ]
            sample["duplicate_point_maps"] = duplicate_maps[:4]
            sample_failures.append(sample)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O5e/O5f",
            "description": "Tests the proposed (P,W,affine-bijection) parametrization and AGL(2,2) torsor claim.",
        },
        "affine_square_mask_pair_count": len(records),
        "fiber_count_by_selected_plane_and_direction": len(fibers),
        "fiber_size_distribution": counter_json(fiber_size_counter),
        "full_affine_map_count_per_plane_distribution": counter_json(
            full_affine_map_count_counter
        ),
        "distinct_point_map_count_distribution": counter_json(
            distinct_point_map_counter
        ),
        "point_map_multiplicity_pattern_distribution": counter_json(
            point_map_multiplicity_pattern_counter
        ),
        "point_map_mask_pair_count_distribution": counter_json(
            point_map_mask_pair_counter
        ),
        "naive_p_w_phi_parametrization_holds": (
            distinct_point_map_counter == {24: len(fibers)}
        ),
        "mask_refined_p_w_phi_mask_parametrization_holds": (
            point_map_mask_pair_counter == {24: len(fibers)}
            and len(global_refined_keys) == len(records)
        ),
        "agl_torsor_fiber_distribution": counter_json(agl_torsor_counter),
        "agl_torsor_holds_for_all_fibers": agl_torsor_counter == {True: len(fibers)},
        "endpoint_distribution_for_agl_torsor_fibers": counter_json(
            endpoint_counter_by_agl_status[True]
        ),
        "endpoint_distribution_for_non_agl_torsor_fibers": counter_json(
            endpoint_counter_by_agl_status[False]
        ),
        "global_refined_key_count": len(global_refined_keys),
        "sample_successes": sample_successes,
        "sample_failures": sample_failures,
        "interpretation": {
            "o5e_verdict": (
                "The coarse fiber count exists: 24 selected planes times 6 "
                "invertible directions times 24 records.  However, records "
                "are not always parametrized by the affine point-map phi alone."
            ),
            "o5f_verdict": (
                "Only 96 of the 144 (P,W)-fibers realize all 24 affine "
                "bijections and hence carry the naive AGL(2,2) torsor on phi. "
                "The remaining 48 fibers have duplicated phi maps."
            ),
            "corrected_parametrization": (
                "The pair (phi, mask) is injective inside every (P,W)-fiber, "
                "so the 24-factor is a mask-refined incidence fiber, not a "
                "pure AGL(2,2) point-map torsor."
            ),
        },
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# O5e/O5f Torsor Parametrization Audit",
        "",
        "Status: Phase O5e/O5f follow-up audit, outside the paper",
        "",
        "## Question",
        "",
        "Do the `3456` affine square-mask pairs admit the clean parametrization",
        "",
        "```text",
        "selected plane P x invertible direction W x affine bijection phi",
        "```",
        "",
        "with the last factor equal to the full `AGL(2,2)` set of `24` affine",
        "bijections?",
        "",
        "## Verdict",
        "",
        "Not in this naive form.",
        "",
        "The coarse fiber count is correct:",
        "",
        f"- affine square-mask pairs: `{result['affine_square_mask_pair_count']}`",
        f"- `(P,W)` fibers: `{result['fiber_count_by_selected_plane_and_direction']}`",
        f"- fiber sizes: `{result['fiber_size_distribution']}`",
        "",
        "But `phi` alone is not always injective in a `(P,W)` fiber:",
        "",
        f"- distinct point-map counts: `{result['distinct_point_map_count_distribution']}`",
        f"- naive `(P,W,phi)` parametrization holds: `{result['naive_p_w_phi_parametrization_holds']}`",
        f"- AGL torsor fibers: `{result['agl_torsor_fiber_distribution']}`",
        f"- AGL torsor holds for all fibers: `{result['agl_torsor_holds_for_all_fibers']}`",
        "",
        "Only `96` of the `144` fibers realize all `24` affine bijections.",
        "",
        "## Corrected Finite Statement",
        "",
        "The mask-refined key is injective:",
        "",
        "```text",
        "(P, W, phi, mask)",
        "```",
        "",
        f"- point-map/mask pair counts: `{result['point_map_mask_pair_count_distribution']}`",
        f"- mask-refined parametrization holds: `{result['mask_refined_p_w_phi_mask_parametrization_holds']}`",
        f"- global refined key count: `{result['global_refined_key_count']}`",
        "",
        "Thus the final `24` factor is real, but it is not uniformly the",
        "`24` affine point maps.  It is a mask-refined incidence fiber.",
        "",
        "## Guardrail",
        "",
        "Do not claim a global `P x W x AGL(2,2)` parametrization of the",
        "`3456` affine square-mask pairs.  The `AGL(2,2)` reading is valid for",
        "a large subfamily (`96` fibers) but not all fibers.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_torsor_parametrization_o5e_o5f()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "torsor_parametrization_o5e_o5f.json"
        report_path = root / "results" / "TORSOR_PARAMETRIZATION_O5E_O5F_REPORT.md"
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
