"""Phase P2: anchored Johnson profiles for the 144/32 boundary.

Phase P1 showed that mask-stratified Johnson data separates the main
176-pair selected-affine signature from the 60 outside-main records, but not
the 144 exact-V4 records from the 32 selected-affine extras.

This refinement anchors the terminal quaterne family against the fixed
translation V4 diagonals

    0123, 1032, 2301, 3210.

For each terminal quaterne Q, we record the sorted vector of intersections
with those four anchor diagonals.  This is still Johnson-scheme data, but
colored by the O5 translation anchor.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_johnson_quaterne_layer_p as phase_p


FIXED_TRANSLATION_V4 = ("0123", "1032", "2301", "3210")


def anchor_quads(names: tuple[str, ...] | list[str]) -> list[phase_p.Quad]:
    return [phase_p.mask_quad(phase_p.perm_from_string(name)) for name in names]


def terminal_quads(
    square: phase_p.Square, mask_perm: phase_p.Perm
) -> tuple[list[phase_p.Quad], list[phase_p.Quad]]:
    mask = phase_p.mask_quad(mask_perm)
    values = [phase_p.square_value(square, idx) for idx in mask]
    t_max = min(v - 1 for v in values)
    target = 34 - t_max

    terminal = []
    terminal_affine = []
    for quad in phase_p.ALL_QUADS:
        source_sum = phase_p.quad_sum(square, quad)
        incidence = phase_p.quad_incidence(quad, mask)
        if source_sum - t_max * incidence == target:
            terminal.append(quad)
            if phase_p.is_value_affine_plane(square, quad):
                terminal_affine.append(quad)
    return terminal, terminal_affine


def anchored_profile(
    quads: list[phase_p.Quad], anchors: list[phase_p.Quad]
) -> dict[str, int]:
    counter: Counter[tuple[int, ...]] = Counter()
    for quad in quads:
        qset = set(quad)
        vector = tuple(
            sorted((len(qset & set(anchor)) for anchor in anchors), reverse=True)
        )
        counter[vector] += 1
    return {",".join(map(str, key)): counter[key] for key in sorted(counter)}


def signature(profile: object) -> str:
    return json.dumps(profile, sort_keys=True, separators=(",", ":"))


def summarize(records: list[dict], field: str) -> dict:
    by_class: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        by_class[record["class"]][signature(record[field])] += 1

    classes = sorted(by_class)
    intersections = {}
    for a, b in itertools.combinations(classes, 2):
        intersections[f"{a}__{b}"] = len(set(by_class[a]) & set(by_class[b]))

    return {
        "field": field,
        "signature_counts": {c: len(by_class[c]) for c in classes},
        "pairwise_intersections": intersections,
        "separates_exact_144_from_extra_32": (
            intersections.get("exact_v4__extra32", 1) == 0
        ),
        "separates_all_classes": all(v == 0 for v in intersections.values()),
        "top_by_class": {
            c: [
                {"count": count, "signature": json.loads(sig)}
                for sig, count in by_class[c].most_common(8)
            ]
            for c in classes
        },
    }


def build_audit(root: Path) -> dict:
    squares = phase_p.load_essential_squares(root)
    classes = phase_p.load_terminal24_classes(root)
    pairs = phase_p.load_terminal24_pairs(root)
    fixed_anchors = anchor_quads(FIXED_TRANSLATION_V4)

    records = []
    for pair in pairs:
        key = (pair["square_index"], pair["mask"])
        square = squares[key[0]]
        mask = phase_p.perm_from_string(key[1])
        terminal, terminal_affine = terminal_quads(square, mask)
        record_anchors = anchor_quads(pair["terminal_diagonal_set"])
        records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "class": classes[key],
                "terminal_set": pair["terminal_diagonal_set"],
                "terminal_set_size": len(pair["terminal_diagonal_set"]),
                "fixed_translation_terminal_anchor_profile": anchored_profile(
                    terminal, fixed_anchors
                ),
                "fixed_translation_terminal_affine_anchor_profile": anchored_profile(
                    terminal_affine, fixed_anchors
                ),
                "record_terminal_anchor_profile": anchored_profile(
                    terminal, record_anchors
                ),
                "record_terminal_affine_anchor_profile": anchored_profile(
                    terminal_affine, record_anchors
                ),
            }
        )

    fields = [
        "fixed_translation_terminal_anchor_profile",
        "fixed_translation_terminal_affine_anchor_profile",
        "record_terminal_anchor_profile",
        "record_terminal_affine_anchor_profile",
    ]

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "P2",
            "description": "Anchored Johnson profiles against the fixed translation V4 and record terminal diagonals.",
            "fixed_translation_v4": list(FIXED_TRANSLATION_V4),
        },
        "class_counts": dict(Counter(record["class"] for record in records)),
        "terminal_set_size_by_class": {
            c: dict(Counter(r["terminal_set_size"] for r in records if r["class"] == c))
            for c in sorted({r["class"] for r in records})
        },
        "profile_summaries": [summarize(records, field) for field in fields],
        "interpretation": {
            "positive": "Anchoring Johnson profiles by the fixed translation V4 separates exact_v4, extra32, and outside_main.",
            "strongest_nontrivial_anchor": "fixed_translation_terminal_affine_anchor_profile",
            "guardrail": "This uses the O5 translation anchor; it is not a mask-only Johnson invariant.",
        },
        "sample_records": records[:5],
    }


def write_report(result: dict, root: Path) -> None:
    lines = [
        "# Phase P2 Anchored Johnson Refinement",
        "",
        "## Class Counts",
        "",
        "```text",
        json.dumps(result["class_counts"], sort_keys=True),
        "```",
        "",
        "## Terminal Set Sizes",
        "",
        "```text",
        json.dumps(result["terminal_set_size_by_class"], sort_keys=True),
        "```",
        "",
        "## Profile Separation",
        "",
        "```text",
    ]
    for row in result["profile_summaries"]:
        lines.append(
            f"{row['field']}: counts={row['signature_counts']} "
            f"intersections={row['pairwise_intersections']} "
            f"exact_vs_extra={row['separates_exact_144_from_extra_32']} "
            f"all={row['separates_all_classes']}"
        )
    lines.extend(
        [
            "```",
            "",
            "## Interpretation",
            "",
            "The mask-only Johnson profiles from P1 do not separate `144` from",
            "`32`.  Anchoring the terminal quaterne family against the fixed",
            "translation `V4 = {0123,1032,2301,3210}` does separate the exact",
            "`V4` class, the selected-affine extras, and the outside-main records.",
            "",
            "This is a real refinement, but it uses the O5 translation anchor.  It",
            "should be described as anchored Johnson/association-scheme data, not",
            "as a mask-only Johnson invariant.",
            "",
        ]
    )
    (root / "results" / "JOHNSON_ANCHOR_REFINEMENT_P2_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    result = build_audit(root)
    if args.write:
        out = root / "results" / "johnson_anchor_refinement_p2.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, root)
        print(out)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
