"""Phase P3: direction-level explanation of the anchored Johnson split.

P2 showed that Johnson profiles anchored by the fixed translation V4

    0123, 1032, 2301, 3210

separate the exact-V4 144 records from the 32 selected-affine extras and the
60 outside-main records.  This script explains the exact-V4 profile by
looking at the domain affine directions of the terminal affine quaternes
relative to the translation direction W0.

For a globally affine exact-V4 record, value-affine quaternes are domain
affine planes.  Their intersections with the four W0-cosets are controlled by
the direction relation:

    same direction W0      -> profile 4,0,0,0
    line intersection      -> profile 2,2,0,0
    complementary direction -> profile 1,1,1,1

The expected exact-V4 terminal-affine inventory is:

    directions: same=1, line=5, complement=3
    quaternes:  same=4, line=20, complement=12
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_johnson_anchor_refinement_p2 as phase_p2
import analyze_johnson_quaterne_layer_p as phase_p


def domain_vector(idx: int) -> int:
    row, col = phase_p.cell_from_index(idx)
    return row | (col << 2)


def affine_direction(quad: phase_p.Quad) -> tuple[int, int, int, int] | None:
    vectors = [domain_vector(idx) for idx in quad]
    if vectors[0] ^ vectors[1] ^ vectors[2] ^ vectors[3] != 0:
        return None
    direction = sorted(v ^ vectors[0] for v in vectors)
    if direction[0] != 0 or len(set(direction)) != 4:
        return None
    return tuple(direction)  # type: ignore[return-value]


def relation_to_w0(direction: tuple[int, int, int, int], w0: set[int]) -> str:
    if set(direction) == w0:
        return "same"
    intersection_size = len(set(direction) & w0)
    if intersection_size == 2:
        return "line"
    if intersection_size == 1:
        return "complement"
    return f"unexpected_intersection_{intersection_size}"


def inventory_for_record(square: phase_p.Square, mask: phase_p.Perm, w0: set[int]) -> dict:
    _terminal, terminal_affine = phase_p2.terminal_quads(square, mask)

    quad_counts: Counter[str] = Counter()
    direction_sets: dict[str, set[tuple[int, int, int, int]]] = defaultdict(set)
    non_domain_affine = 0
    for quad in terminal_affine:
        direction = affine_direction(quad)
        if direction is None:
            non_domain_affine += 1
            continue
        relation = relation_to_w0(direction, w0)
        quad_counts[relation] += 1
        direction_sets[relation].add(direction)

    return {
        "terminal_affine_count": len(terminal_affine),
        "non_domain_affine_terminal_affine_count": non_domain_affine,
        "quad_relation_counts": dict(sorted(quad_counts.items())),
        "direction_relation_counts": {
            key: len(value) for key, value in sorted(direction_sets.items())
        },
        "directions_by_relation": {
            key: [".".join(map(str, direction)) for direction in sorted(value)]
            for key, value in sorted(direction_sets.items())
        },
    }


def signature(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def summarize(records: list[dict]) -> dict:
    by_class: dict[str, Counter[str]] = defaultdict(Counter)
    samples: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        sig = signature(
            {
                "non_domain_affine": record["inventory"][
                    "non_domain_affine_terminal_affine_count"
                ],
                "quad_relation_counts": record["inventory"]["quad_relation_counts"],
                "direction_relation_counts": record["inventory"][
                    "direction_relation_counts"
                ],
            }
        )
        by_class[record["class"]][sig] += 1
        if len(samples[record["class"]]) < 3:
            samples[record["class"]].append(record)

    classes = sorted(by_class)
    intersections = {}
    for i, a in enumerate(classes):
        for b in classes[i + 1 :]:
            intersections[f"{a}__{b}"] = len(set(by_class[a]) & set(by_class[b]))

    return {
        "signature_counts": {klass: len(by_class[klass]) for klass in classes},
        "pairwise_intersections": intersections,
        "top_by_class": {
            klass: [
                {"count": count, "signature": json.loads(sig)}
                for sig, count in by_class[klass].most_common(8)
            ]
            for klass in classes
        },
        "samples": samples,
    }


def build_audit(root: Path) -> dict:
    squares = phase_p.load_essential_squares(root)
    classes = phase_p.load_terminal24_classes(root)
    pairs = phase_p.load_terminal24_pairs(root)
    w0_direction = affine_direction(phase_p.mask_quad(phase_p.perm_from_string("0123")))
    if w0_direction is None:
        raise RuntimeError("fixed translation anchor is not a domain affine plane")
    w0 = set(w0_direction)

    records = []
    for pair in pairs:
        key = (pair["square_index"], pair["mask"])
        square = squares[key[0]]
        mask = phase_p.perm_from_string(key[1])
        records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "class": classes[key],
                "terminal_set": pair["terminal_diagonal_set"],
                "inventory": inventory_for_record(square, mask, w0),
            }
        )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "P3",
            "description": "Direction-level explanation of fixed-translation anchored Johnson profiles.",
            "fixed_translation_v4": list(phase_p2.FIXED_TRANSLATION_V4),
            "fixed_translation_direction": ".".join(map(str, w0_direction)),
        },
        "class_counts": dict(Counter(record["class"] for record in records)),
        "summary": summarize(records),
        "interpretation": {
            "exact_v4": "The exact 144 have the uniform terminal-affine direction inventory same=1, line=5, complement=3 and no non-domain-affine terminal affine quaternes.",
            "anchored_profile_meaning": "The P2 profiles 4,0,0,0 / 2,2,0,0 / 1,1,1,1 are the coset-intersection shadows of same / line / complement direction relations relative to the fixed translation V4 partition.",
            "guardrail": "This explains the O5-anchored split. It is not a mask-only Johnson invariant and it does not explain the strong meet itself.",
        },
    }


def write_report(result: dict, root: Path) -> None:
    lines = [
        "# Phase P3 Johnson Anchor Direction Audit",
        "",
        "## Class Counts",
        "",
        "```text",
        json.dumps(result["class_counts"], sort_keys=True),
        "```",
        "",
        "## Direction Signature Summary",
        "",
        "```text",
        f"signature_counts={result['summary']['signature_counts']}",
        f"pairwise_intersections={result['summary']['pairwise_intersections']}",
        "```",
        "",
        "## Top Signatures",
        "",
    ]
    for klass, rows in result["summary"]["top_by_class"].items():
        lines.append(f"### {klass}")
        lines.append("")
        lines.append("```text")
        for row in rows:
            lines.append(f"count={row['count']} signature={json.dumps(row['signature'], sort_keys=True)}")
        lines.append("```")
        lines.append("")
    lines.extend(
        [
            "## Interpretation",
            "",
            "Relative to the fixed translation `V4` partition, an affine quaterne",
            "with the same direction as the anchor has profile `4,0,0,0`; a",
            "direction meeting the anchor in a line has profile `2,2,0,0`; and",
            "a complementary direction has profile `1,1,1,1`.",
            "",
            "The exact `144` records have a uniform terminal-affine direction",
            "inventory:",
            "",
            "```text",
            "same direction:       1 direction,  4 quaternes",
            "line intersection:    5 directions, 20 quaternes",
            "complement direction: 3 directions, 12 quaternes",
            "non-domain-affine terminal affine quaternes: 0",
            "```",
            "",
            "Thus the exact P2 terminal-affine anchored profile",
            "`4*(4,0,0,0) + 20*(2,2,0,0) + 12*(1,1,1,1)` is not a",
            "mysterious fingerprint; it is the quotient shadow of a uniform",
            "`1+5+3` direction inventory relative to the fixed translation",
            "direction.",
            "",
            "The selected-affine extras and outside-main records do not share",
            "this direction inventory.  This explains why the O5-anchored",
            "Johnson profile separates the `144` from the `32`, while the",
            "mask-only Johnson profile does not.",
            "",
        ]
    )
    (root / "results" / "JOHNSON_ANCHOR_DIRECTION_P3_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    result = build_audit(root)
    if args.write:
        out = root / "results" / "johnson_anchor_direction_p3.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, root)
        print(out)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
