"""Phase P5: O5e collision table and the forbidden-shadow obstruction.

This closes two follow-up questions:

1. O5e collision table.  For each direction pair (U,W), where U is the
   selected-plane direction and W is the translation direction, record the
   point-map collision type in the (P,W)-fibers.  The finite pattern should
   be a matching with 0, 4, or 8 collision edges.

2. Forbidden quotient-shadow obstruction.  Relative to the fixed translation
   spread W0, a domain-affine plane can only have sorted block shadow
   4,0,0,0 / 2,2,0,0 / 1,1,1,1.  Thus 2,1,1,0 is a certificate that a
   terminal value-affine quaterne is not domain-affine.  This separates the
   exact 144 from the 32 selected-affine extras inside the main 176.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

import analyze_affine_normal_layer as affine_layer
import analyze_johnson_anchor_direction_p3 as p3
import analyze_johnson_anchor_refinement_p2 as p2
import analyze_johnson_quaterne_layer_p as phase_p
import analyze_terminal_parallel_torsor_o5b as torsor
import analyze_torsor_parametrization_o5e_o5f as o5e


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def signature(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def fixed_w0() -> set[int]:
    direction = p3.affine_direction(phase_p.mask_quad(phase_p.perm_from_string("0123")))
    if direction is None:
        raise RuntimeError("fixed translation anchor is not affine")
    return set(direction)


def all_domain_affine_planes() -> list[phase_p.Quad]:
    planes = []
    for quad in phase_p.ALL_QUADS:
        if p3.affine_direction(quad) is not None:
            planes.append(quad)
    return planes


def shadow_key(quad: phase_p.Quad) -> str:
    anchors = p2.anchor_quads(p2.FIXED_TRANSLATION_V4)
    vector = [len(set(quad) & set(anchor)) for anchor in anchors]
    return ",".join(map(str, sorted(vector, reverse=True)))


def collision_table() -> dict:
    o2 = affine_layer.build_affine_normal_layer()
    root = Path(__file__).resolve().parents[1]
    dataset = json.loads((root / "data" / "order4_normal_essential_880.json").read_text())
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]

    fibers: dict[tuple[tuple[int, ...], tuple[int, ...]], list[dict]] = defaultdict(list)
    for record in o2["records"]:
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
                "point_map": o5e.point_map_key(profile),
            }
        )

    fiber_rows = []
    direction_pair_rows: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for (selected_plane, translation_direction), records in sorted(
        fibers.items(), key=lambda item: (o5e.plane_key(item[0][0]), o5e.direction_key(item[0][1]))
    ):
        point_map_counts = Counter(record["point_map"] for record in records)
        multiplicities = sorted(point_map_counts.values(), reverse=True)
        collision_edges = sum(comb(count, 2) for count in point_map_counts.values())
        duplicate_maps = sum(1 for count in point_map_counts.values() if count > 1)
        max_multiplicity = max(multiplicities)
        selected_direction = o5e.direction_key(o5e.direction_of_plane(selected_plane))
        translation_key = o5e.direction_key(translation_direction)
        row = {
            "selected_plane": o5e.plane_key(selected_plane),
            "selected_plane_direction": selected_direction,
            "translation_direction": translation_key,
            "record_count": len(records),
            "distinct_point_maps": len(point_map_counts),
            "collision_edges": collision_edges,
            "duplicate_point_maps": duplicate_maps,
            "max_point_map_multiplicity": max_multiplicity,
            "multiplicity_pattern": ",".join(map(str, multiplicities)),
            "endpoint_distribution": counter_json(Counter(r["endpoint"] for r in records)),
            "mask_distribution": counter_json(Counter(r["mask"] for r in records)),
        }
        fiber_rows.append(row)
        direction_pair_rows[(selected_direction, translation_key)].append(row)

    direction_table = []
    ambiguous_direction_pairs = {}
    for (selected_direction, translation_direction), rows in sorted(direction_pair_rows.items()):
        distinct_types = sorted({row["distinct_point_maps"] for row in rows})
        collision_edges = sorted({row["collision_edges"] for row in rows})
        duplicate_maps = sorted({row["duplicate_point_maps"] for row in rows})
        if len(distinct_types) != 1 or len(collision_edges) != 1:
            ambiguous_direction_pairs[
                f"{selected_direction} | {translation_direction}"
            ] = {
                "distinct_point_maps": distinct_types,
                "collision_edges": collision_edges,
            }
        direction_table.append(
            {
                "selected_plane_direction": selected_direction,
                "translation_direction": translation_direction,
                "fiber_count": len(rows),
                "distinct_point_maps": distinct_types[0],
                "collision_edges": collision_edges[0],
                "duplicate_point_maps": duplicate_maps[0],
            }
        )

    return {
        "fiber_count": len(fiber_rows),
        "direction_pair_count": len(direction_table),
        "distinct_point_map_distribution": counter_json(
            Counter(row["distinct_point_maps"] for row in fiber_rows)
        ),
        "collision_edge_distribution": counter_json(
            Counter(row["collision_edges"] for row in fiber_rows)
        ),
        "duplicate_point_map_distribution": counter_json(
            Counter(row["duplicate_point_maps"] for row in fiber_rows)
        ),
        "max_multiplicity_distribution": counter_json(
            Counter(row["max_point_map_multiplicity"] for row in fiber_rows)
        ),
        "matching_collision_graph_holds": all(
            row["max_point_map_multiplicity"] <= 2
            and row["collision_edges"] == row["duplicate_point_maps"]
            for row in fiber_rows
        ),
        "direction_pair_classifier_holds": not ambiguous_direction_pairs,
        "ambiguous_direction_pairs": ambiguous_direction_pairs,
        "direction_pair_table": direction_table,
        "sample_fibers": fiber_rows[:8],
    }


def forbidden_shadow_audit(root: Path) -> dict:
    w0 = fixed_w0()
    domain_planes = all_domain_affine_planes()
    ambient_shadow_profile = Counter(shadow_key(quad) for quad in domain_planes)

    squares = phase_p.load_essential_squares(root)
    classes = phase_p.load_terminal24_classes(root)
    pairs = phase_p.load_terminal24_pairs(root)

    records = []
    for pair in pairs:
        key = (pair["square_index"], pair["mask"])
        square = squares[key[0]]
        mask = phase_p.perm_from_string(key[1])
        _terminal, terminal_affine = p2.terminal_quads(square, mask)
        shadow_profile = Counter(shadow_key(quad) for quad in terminal_affine)
        domain_inventory = p3.inventory_for_record(square, mask, w0)
        records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "class": classes[key],
                "terminal_affine_count": len(terminal_affine),
                "shadow_profile": counter_json(shadow_profile),
                "F_1111": shadow_profile.get("1,1,1,1", 0),
                "F_2200": shadow_profile.get("2,2,0,0", 0),
                "F_4000": shadow_profile.get("4,0,0,0", 0),
                "F_2110": shadow_profile.get("2,1,1,0", 0),
                "non_domain_affine": domain_inventory[
                    "non_domain_affine_terminal_affine_count"
                ],
            }
        )

    main_records = [r for r in records if r["class"] in ("exact_v4", "extra32")]
    invariant_counter = Counter(
        (
            record["class"],
            record["F_1111"],
            record["F_2200"],
            record["F_4000"],
            record["F_2110"],
            record["non_domain_affine"],
        )
        for record in main_records
    )
    invariant_rows = [
        {
            "class": key[0],
            "F_1111": key[1],
            "F_2200": key[2],
            "F_4000": key[3],
            "F_2110": key[4],
            "non_domain_affine": key[5],
            "count": count,
        }
        for key, count in sorted(invariant_counter.items())
    ]

    exact_iff_zero_forbidden = all(
        (record["class"] == "exact_v4") == (record["F_2110"] == 0)
        for record in main_records
    )
    forbidden_equals_non_domain = all(
        record["F_2110"] == record["non_domain_affine"]
        for record in main_records
    )

    return {
        "ambient_domain_affine_plane_count": len(domain_planes),
        "ambient_domain_affine_shadow_profile": counter_json(ambient_shadow_profile),
        "ambient_has_forbidden_2110": ambient_shadow_profile.get("2,1,1,0", 0) > 0,
        "main_176_count": len(main_records),
        "invariant_rows_main_176": invariant_rows,
        "exact_v4_iff_F_2110_zero_inside_main_176": exact_iff_zero_forbidden,
        "F_2110_equals_non_domain_affine_inside_main_176": forbidden_equals_non_domain,
        "class_counts": counter_json(Counter(record["class"] for record in records)),
        "records_sample": records[:8],
        "interpretation": {
            "forbidden_shadow": "The shadow 2,1,1,0 cannot occur for a domain-affine plane under the quotient by the fixed translation spread.",
            "extra32": "Inside the main 176, the 32 extras are exactly the records with positive forbidden-shadow mass F_2110.",
        },
    }


def build_audit(root: Path) -> dict:
    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "P5",
            "description": "O5e collision-matching table and forbidden quotient-shadow obstruction for the 32 extras.",
        },
        "o5e_collision_table": collision_table(),
        "forbidden_shadow_obstruction": forbidden_shadow_audit(root),
        "interpretation": {
            "o5e": "Every O5e fiber collision graph is a matching with 0, 4, or 8 collision edges; the direction pair (U,W) classifies the type.",
            "extra32": "The missing invariant for the 32 extras is positive forbidden quotient-shadow mass F_2110 relative to the fixed translation spread.",
            "guardrail": "P5 is affine/atlas follow-up structure, not a new proof of the strong meet.",
        },
    }


def write_report(result: dict, root: Path) -> None:
    collision = result["o5e_collision_table"]
    forbidden = result["forbidden_shadow_obstruction"]
    lines = [
        "# Phase P5 Collision And Forbidden-Shadow Audit",
        "",
        "## O5e Collision-Matching Table",
        "",
        "```text",
        f"fiber_count={collision['fiber_count']}",
        f"direction_pair_count={collision['direction_pair_count']}",
        f"distinct_point_map_distribution={collision['distinct_point_map_distribution']}",
        f"collision_edge_distribution={collision['collision_edge_distribution']}",
        f"max_multiplicity_distribution={collision['max_multiplicity_distribution']}",
        f"matching_collision_graph_holds={collision['matching_collision_graph_holds']}",
        f"direction_pair_classifier_holds={collision['direction_pair_classifier_holds']}",
        "```",
        "",
        "Direction-pair table:",
        "",
        "```text",
    ]
    for row in collision["direction_pair_table"]:
        lines.append(
            f"U={row['selected_plane_direction']} W={row['translation_direction']} "
            f"fibers={row['fiber_count']} maps={row['distinct_point_maps']} "
            f"edges={row['collision_edges']}"
        )
    lines.extend(
        [
            "```",
            "",
            "## Forbidden Quotient-Shadow Obstruction",
            "",
            "Domain-affine planes relative to the fixed translation spread have",
            "only the quotient shadows `4,0,0,0`, `2,2,0,0`, and `1,1,1,1`:",
            "",
            "```text",
            f"ambient_domain_affine_plane_count={forbidden['ambient_domain_affine_plane_count']}",
            f"ambient_domain_affine_shadow_profile={forbidden['ambient_domain_affine_shadow_profile']}",
            f"ambient_has_forbidden_2110={forbidden['ambient_has_forbidden_2110']}",
            "```",
            "",
            "Inside the main `176 = 144 + 32` selected-affine signature:",
            "",
            "```text",
        ]
    )
    for row in forbidden["invariant_rows_main_176"]:
        lines.append(
            f"{row['class']} count={row['count']} "
            f"F1111={row['F_1111']} F2200={row['F_2200']} "
            f"F4000={row['F_4000']} F2110={row['F_2110']} "
            f"non_domain={row['non_domain_affine']}"
        )
    lines.extend(
        [
            f"exact_v4_iff_F2110_zero={forbidden['exact_v4_iff_F_2110_zero_inside_main_176']}",
            f"F2110_equals_non_domain={forbidden['F_2110_equals_non_domain_affine_inside_main_176']}",
            "```",
            "",
            "## Interpretation",
            "",
            "The O5e collision graph is always a matching: no point-map has",
            "multiplicity above `2`.  The three cases have `0`, `4`, or `8`",
            "collision edges, and the direction pair `(U,W)` classifies which",
            "case occurs.",
            "",
            "The `32` extras are no longer just unexplained near-misses.  Within",
            "the main `176` signature, exact-`V4` is equivalent to zero",
            "forbidden-shadow mass `F_2110=0`; the `32` extras are exactly the",
            "positive forbidden-shadow records, split as `F_2110=12` and",
            "`F_2110=16`.",
            "",
        ]
    )
    (root / "results" / "O5E_COLLISION_FORBIDDEN_SHADOW_P5_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = build_audit(root)
    if args.write:
        out = root / "results" / "o5e_collision_forbidden_shadow_p5.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, root)
        print(out)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
