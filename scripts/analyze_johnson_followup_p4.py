"""Phase P4: Johnson/design follow-up and O5e collision stratification.

This is a targeted follow-up to P1/P2/P3.  It keeps two questions separate:

1. For the terminal-24 atlas, do the terminal affine quaternes have a
   design/code signature that explains the P3 exact-V4 profile?
2. For the global affine O5e/O5f layer, are the point-map collisions
   (24/20/16 distinct maps per (P,W)-fiber) explained by a simple endpoint,
   plane, mask, or anchor-shadow invariant?

The audit is deliberately finite and descriptive.  It does not promote the
Johnson layer to a proof of the strong meet.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_affine_normal_layer as affine_layer
import analyze_johnson_anchor_direction_p3 as phase_p3
import analyze_johnson_anchor_refinement_p2 as phase_p2
import analyze_johnson_quaterne_layer_p as phase_p
import analyze_torsor_parametrization_o5e_o5f as o5e
import analyze_terminal_parallel_torsor_o5b as torsor


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def sorted_vector_key(values: list[int] | tuple[int, ...]) -> str:
    return ",".join(map(str, sorted(values, reverse=True)))


def anchor_index_by_cell() -> dict[int, int]:
    anchors = phase_p2.anchor_quads(phase_p2.FIXED_TRANSLATION_V4)
    result = {}
    for anchor_idx, anchor in enumerate(anchors):
        for cell in anchor:
            result[cell] = anchor_idx
    return result


ANCHOR_BY_CELL = anchor_index_by_cell()


def inner_distribution(quads: list[phase_p.Quad]) -> dict[str, int]:
    counter: Counter[int] = Counter()
    for a, b in itertools.combinations(quads, 2):
        counter[len(set(a) & set(b))] += 1
    return counter_json(counter)


def point_degree_profile(quads: list[phase_p.Quad]) -> dict[str, int]:
    degrees: Counter[int] = Counter()
    for quad in quads:
        for cell in quad:
            degrees[cell] += 1
    return counter_json(Counter(degrees.get(cell, 0) for cell in range(16)))


def pair_degree_profiles(quads: list[phase_p.Quad]) -> dict[str, dict[str, int]]:
    pair_degrees: Counter[tuple[int, int]] = Counter()
    for quad in quads:
        for a, b in itertools.combinations(sorted(quad), 2):
            pair_degrees[(a, b)] += 1

    same_block: Counter[int] = Counter()
    different_block: Counter[int] = Counter()
    all_pairs: Counter[int] = Counter()
    for a, b in itertools.combinations(range(16), 2):
        degree = pair_degrees.get((a, b), 0)
        all_pairs[degree] += 1
        if ANCHOR_BY_CELL[a] == ANCHOR_BY_CELL[b]:
            same_block[degree] += 1
        else:
            different_block[degree] += 1

    return {
        "all": counter_json(all_pairs),
        "same_anchor_block": counter_json(same_block),
        "different_anchor_block": counter_json(different_block),
    }


def anchor_shadow_profile(quads: list[phase_p.Quad]) -> dict[str, int]:
    anchors = phase_p2.anchor_quads(phase_p2.FIXED_TRANSLATION_V4)
    return phase_p2.anchored_profile(quads, anchors)


def domain_direction_inventory(quads: list[phase_p.Quad], w0: set[int]) -> dict:
    quad_counts: Counter[str] = Counter()
    direction_sets: dict[str, set[tuple[int, int, int, int]]] = defaultdict(set)
    non_domain_affine = 0
    for quad in quads:
        direction = phase_p3.affine_direction(quad)
        if direction is None:
            non_domain_affine += 1
            continue
        relation = phase_p3.relation_to_w0(direction, w0)
        quad_counts[relation] += 1
        direction_sets[relation].add(direction)
    return {
        "non_domain_affine": non_domain_affine,
        "quad_relation_counts": dict(sorted(quad_counts.items())),
        "direction_relation_counts": {
            key: len(value) for key, value in sorted(direction_sets.items())
        },
    }


def code_profile(quads: list[phase_p.Quad], w0: set[int]) -> dict:
    return {
        "count": len(quads),
        "inner_distribution": inner_distribution(quads),
        "point_degree_profile": point_degree_profile(quads),
        "pair_degree_profiles": pair_degree_profiles(quads),
        "anchor_shadow_profile": anchor_shadow_profile(quads),
        "domain_direction_inventory": domain_direction_inventory(quads, w0),
    }


def signature(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def summarize_code_profiles(records: list[dict], field: str) -> dict:
    by_class: dict[str, Counter[str]] = defaultdict(Counter)
    top_profiles: dict[str, list[dict]] = {}
    for record in records:
        by_class[record["class"]][signature(record[field])] += 1

    for klass, counts in by_class.items():
        top_profiles[klass] = [
            {"count": count, "signature": json.loads(sig)}
            for sig, count in counts.most_common(6)
        ]

    classes = sorted(by_class)
    intersections = {}
    for i, a in enumerate(classes):
        for b in classes[i + 1 :]:
            intersections[f"{a}__{b}"] = len(set(by_class[a]) & set(by_class[b]))

    return {
        "field": field,
        "signature_counts": {klass: len(by_class[klass]) for klass in classes},
        "pairwise_intersections": intersections,
        "top_by_class": top_profiles,
    }


def build_terminal24_code_audit(root: Path) -> dict:
    squares = phase_p.load_essential_squares(root)
    classes = phase_p.load_terminal24_classes(root)
    pairs = phase_p.load_terminal24_pairs(root)
    w0_direction = phase_p3.affine_direction(
        phase_p.mask_quad(phase_p.perm_from_string("0123"))
    )
    if w0_direction is None:
        raise RuntimeError("fixed translation anchor is not affine")
    w0 = set(w0_direction)

    records = []
    for pair in pairs:
        key = (pair["square_index"], pair["mask"])
        square = squares[key[0]]
        mask = phase_p.perm_from_string(key[1])
        terminal, terminal_affine = phase_p2.terminal_quads(square, mask)
        records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "class": classes[key],
                "terminal_profile": code_profile(terminal, w0),
                "terminal_affine_profile": code_profile(terminal_affine, w0),
            }
        )

    return {
        "class_counts": dict(Counter(record["class"] for record in records)),
        "summaries": [
            summarize_code_profiles(records, "terminal_profile"),
            summarize_code_profiles(records, "terminal_affine_profile"),
        ],
        "exact_terminal_affine_signature": next(
            row
            for row in summarize_code_profiles(records, "terminal_affine_profile")[
                "top_by_class"
            ]["exact_v4"]
            if row["count"] == 144
        )["signature"],
    }


def selected_plane_min(plane: tuple[int, ...]) -> int:
    return min(value + 1 for value in plane)


def selected_plane_direction_key(plane: tuple[int, ...]) -> str:
    return o5e.direction_key(o5e.direction_of_plane(plane))


def selected_plane_anchor_shadow(plane: tuple[int, ...]) -> str:
    # Plane points are values 0..15.  Interpret them through Durer value-cell
    # labels, where value v sits in the cell whose Durer value is v+1.
    value_to_cell = {}
    for cell in range(16):
        value_to_cell[phase_p.square_value(phase_p.DURER_COMPLEMENT, cell) - 1] = cell
    quad = tuple(sorted(value_to_cell[value] for value in plane))
    anchors = phase_p2.anchor_quads(phase_p2.FIXED_TRANSLATION_V4)
    vector = [
        len(set(quad) & set(anchor))
        for anchor in anchors
    ]
    return sorted_vector_key(vector)


def build_o5e_collision_audit() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    records = o2["records"]
    root = Path(__file__).resolve().parents[1]
    dataset = json.loads((root / "data" / "order4_normal_essential_880.json").read_text())
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
                "point_map": o5e.point_map_key(profile),
            }
        )

    fiber_records = []
    for (selected_plane, translation_direction), fiber in sorted(
        fibers.items(), key=lambda item: (o5e.plane_key(item[0][0]), o5e.direction_key(item[0][1]))
    ):
        point_map_counts = Counter(record["point_map"] for record in fiber)
        endpoint_counter = Counter(record["endpoint"] for record in fiber)
        mask_counter = Counter(record["mask"] for record in fiber)
        terminal_full_counter = Counter(
            record["terminal_set_is_full_translation_v4"] for record in fiber
        )
        distinct_point_maps = len(point_map_counts)
        duplicate_pattern = tuple(sorted(point_map_counts.values(), reverse=True))
        fiber_records.append(
            {
                "selected_plane": o5e.plane_key(selected_plane),
                "selected_plane_min": selected_plane_min(selected_plane),
                "selected_plane_direction": selected_plane_direction_key(selected_plane),
                "selected_plane_anchor_shadow": selected_plane_anchor_shadow(selected_plane),
                "translation_direction": o5e.direction_key(translation_direction),
                "distinct_point_maps": distinct_point_maps,
                "duplicate_pattern": list(duplicate_pattern),
                "endpoint_distribution": counter_json(endpoint_counter),
                "mask_distribution": counter_json(mask_counter),
                "terminal_full_translation_distribution": counter_json(
                    terminal_full_counter
                ),
            }
        )

    fields = [
        "selected_plane",
        "selected_plane_min",
        "selected_plane_direction",
        "selected_plane_anchor_shadow",
        "translation_direction",
        "endpoint_distribution",
        "mask_distribution",
        "terminal_full_translation_distribution",
    ]
    by_collision: dict[int, list[dict]] = defaultdict(list)
    for record in fiber_records:
        by_collision[record["distinct_point_maps"]].append(record)

    selected_plane_collision_patterns: Counter[str] = Counter()
    by_selected_plane: dict[str, Counter[int]] = defaultdict(Counter)
    for record in fiber_records:
        by_selected_plane[record["selected_plane"]][record["distinct_point_maps"]] += 1
    for counts in by_selected_plane.values():
        selected_plane_collision_patterns[signature(dict(sorted(counts.items())))] += 1

    selected_plane_direction_collision_distribution = {
        direction: counter_json(Counter(record["distinct_point_maps"] for record in rows))
        for direction, rows in sorted(
            {
                direction: [
                    record
                    for record in fiber_records
                    if record["selected_plane_direction"] == direction
                ]
                for direction in {
                    record["selected_plane_direction"] for record in fiber_records
                }
            }.items()
        )
    }

    joint_direction_keys: dict[tuple[str, str], set[int]] = defaultdict(set)
    for record in fiber_records:
        joint_direction_keys[
            (record["selected_plane_direction"], record["translation_direction"])
        ].add(record["distinct_point_maps"])
    ambiguous_joint_direction_keys = {
        f"{key[0]} | {key[1]}": sorted(values)
        for key, values in sorted(joint_direction_keys.items())
        if len(values) > 1
    }

    field_summaries = {}
    for field in fields:
        field_summaries[field] = {
            str(collision): counter_json(Counter(signature(record[field]) for record in rows))
            for collision, rows in sorted(by_collision.items())
        }

    combined_signature_counts = {
        str(collision): counter_json(
            Counter(
                signature(
                    {
                        "selected_plane_min": record["selected_plane_min"],
                        "selected_plane_anchor_shadow": record[
                            "selected_plane_anchor_shadow"
                        ],
                        "endpoint_distribution": record["endpoint_distribution"],
                        "mask_distribution": record["mask_distribution"],
                        "terminal_full_translation_distribution": record[
                            "terminal_full_translation_distribution"
                        ],
                    }
                )
                for record in rows
            )
        )
        for collision, rows in sorted(by_collision.items())
    }

    return {
        "fiber_count": len(fiber_records),
        "distinct_point_map_count_distribution": counter_json(
            Counter(record["distinct_point_maps"] for record in fiber_records)
        ),
        "field_summaries_by_distinct_point_maps": field_summaries,
        "selected_plane_collision_pattern_distribution": {
            key: selected_plane_collision_patterns[key]
            for key in sorted(selected_plane_collision_patterns)
        },
        "selected_plane_direction_collision_distribution": (
            selected_plane_direction_collision_distribution
        ),
        "joint_selected_direction_translation_direction_classifier": {
            "joint_key_count": len(joint_direction_keys),
            "ambiguous_joint_key_count": len(ambiguous_joint_direction_keys),
            "ambiguous_joint_keys": ambiguous_joint_direction_keys,
        },
        "combined_signature_counts_by_distinct_point_maps": combined_signature_counts,
        "sample_by_collision_type": {
            str(collision): rows[:3] for collision, rows in sorted(by_collision.items())
        },
        "interpretation": {
            "negative": "No single tested coarse field by itself explains the 24/20/16 split for every fiber.",
            "positive": "The pair (selected plane direction, translation direction) classifies the split with no ambiguous joint keys.",
        },
    }


def build_audit(root: Path) -> dict:
    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "P4",
            "description": "Johnson inner distribution, design-strength profiles, quotient shadows, and O5e collision stratification.",
        },
        "terminal24_code_audit": build_terminal24_code_audit(root),
        "o5e_collision_audit": build_o5e_collision_audit(),
        "interpretation": {
            "p4_terminal24": "The exact 144 terminal-affine code has a single uniform profile, while extras/outside split into multiple profiles.",
            "p4_o5e": "The O5e 24/20/16 collision split is not explained by a single coarse field in this audit; it remains a mask-refined incidence phenomenon.",
            "guardrail": "P4 is follow-up structure for the affine/atlas layer, not a new proof of Meet_strong={24}.",
        },
    }


def write_report(result: dict, root: Path) -> None:
    terminal = result["terminal24_code_audit"]
    collision = result["o5e_collision_audit"]
    lines = [
        "# Phase P4 Johnson Follow-Up",
        "",
        "## Terminal-24 Code Profiles",
        "",
        "```text",
        f"class_counts={terminal['class_counts']}",
        "```",
        "",
    ]
    for summary in terminal["summaries"]:
        lines.extend(
            [
                f"### {summary['field']}",
                "",
                "```text",
                f"signature_counts={summary['signature_counts']}",
                f"pairwise_intersections={summary['pairwise_intersections']}",
                "```",
                "",
            ]
        )
        for klass, rows in summary["top_by_class"].items():
            lines.append(f"- {klass}:")
            for row in rows[:3]:
                lines.append(f"  - count={row['count']}")
                lines.append(f"    signature={json.dumps(row['signature'], sort_keys=True)}")
            lines.append("")

    lines.extend(
        [
            "## O5e Collision Stratification",
            "",
            "```text",
            f"fiber_count={collision['fiber_count']}",
            f"distinct_point_map_count_distribution={collision['distinct_point_map_count_distribution']}",
            "```",
            "",
            "The tested coarse fields by collision type are recorded in the JSON.",
            "No single tested coarse field explains the complete `24/20/16`",
            "split for every fiber by itself.  The selected-plane directions",
            "fall into three regimes:",
            "",
            "```text",
        ]
    )
    for direction, distribution in collision[
        "selected_plane_direction_collision_distribution"
    ].items():
        lines.append(f"{direction}: {distribution}")
    lines.extend(
        [
            "```",
            "",
            "Moreover, the joint key",
            "`(selected_plane_direction, translation_direction)` classifies the",
            "collision type with no ambiguity:",
            "",
            "```text",
            f"joint_key_count={collision['joint_selected_direction_translation_direction_classifier']['joint_key_count']}",
            f"ambiguous_joint_key_count={collision['joint_selected_direction_translation_direction_classifier']['ambiguous_joint_key_count']}",
            "```",
            "",
            "## Interpretation",
            "",
            "P4 confirms that the exact `144` terminal-affine layer is a uniform",
            "small constant-weight code relative to the fixed translation spread:",
            "its inner distribution, point degrees, pair degrees, anchor shadow,",
            "and direction inventory all collapse to one signature.  The `32`",
            "extras and the `60` outside-main records do not collapse to that",
            "signature.",
            "",
            "The O5e collision split remains mask-refined, but it is no longer",
            "opaque: the selected-plane direction gives three coarse regimes,",
            "and adding the translation direction determines the exact collision",
            "type.",
            "",
        ]
    )
    (root / "results" / "JOHNSON_FOLLOWUP_P4_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = build_audit(root)
    if args.write:
        out = root / "results" / "johnson_followup_p4.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, root)
        print(out)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
