"""Phase P6: quotient-shadow lemma and the extra-32 split.

This is a small follow-up to P5.  It records two facts:

1. The shadow (2,1,1,0) is forbidden for a domain-affine plane by a
   dimension argument in the quotient by the fixed translation spread.

2. Inside the 32 selected-affine extras, the P5 split F_2110=12/16 is not
   arbitrary: it is exactly the old terminal-set split
   two_diagonal_pair versus the two v4-like classes.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_exact_v4_affine_mechanism as j2
import analyze_johnson_anchor_refinement_p2 as p2
import analyze_johnson_quaterne_layer_p as phase_p
import analyze_o5e_collision_and_forbidden_shadow_p5 as p5


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def profile_key(profile: dict) -> str:
    return json.dumps(profile, sort_keys=True, separators=(",", ":"))


def build_audit(root: Path) -> dict:
    squares = phase_p.load_essential_squares(root)
    classes = phase_p.load_terminal24_classes(root)
    pairs = phase_p.load_terminal24_pairs(root)
    post_j2 = json.loads((root / "results" / "extra32_post_j2_audit.json").read_text())
    post_by_key = {
        (record["square_index"], record["mask"]): record
        for record in post_j2["records"]
    }

    records = []
    for pair in pairs:
        key = (pair["square_index"], pair["mask"])
        if classes[key] != "extra32":
            continue

        square = squares[key[0]]
        mask = phase_p.perm_from_string(key[1])
        _terminal, terminal_affine = p2.terminal_quads(square, mask)
        shadow_profile = Counter(p5.shadow_key(quad) for quad in terminal_affine)
        post = post_by_key[key]
        terminal_profile = j2.terminal_set_profile(post["terminal_diagonal_set"])
        records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "F_1111": shadow_profile.get("1,1,1,1", 0),
                "F_2200": shadow_profile.get("2,2,0,0", 0),
                "F_4000": shadow_profile.get("4,0,0,0", 0),
                "F_2110": shadow_profile.get("2,1,1,0", 0),
                "terminal_set_class": post["terminal_set_class"],
                "terminal_diagonal_set": post["terminal_diagonal_set"],
                "terminal_set_is_translation_subset": terminal_profile[
                    "is_translation_subset"
                ],
                "terminal_translation_offset_count": len(
                    terminal_profile["translation_offsets"]
                ),
                "terminal_linear_part_counts": terminal_profile[
                    "linear_part_counts"
                ],
                "source_diagonal_size": post["source_diagonal_size"],
                "complement_fixed": post["complement_fixed"],
                "mismatch_mask_intersection_count": post[
                    "mismatch_mask_intersection_count"
                ],
                "hilbert_min_atom_count": post["hilbert_min_atom_count"],
                "markov_degree": post["markov_degree"],
            }
        )

    by_f2110: dict[int, list[dict]] = defaultdict(list)
    for record in records:
        by_f2110[record["F_2110"]].append(record)

    terminal_profile_counter: Counter[str] = Counter()
    terminal_profile_examples = {}
    for record in records:
        profile = {
            "terminal_set_class": record["terminal_set_class"],
            "terminal_diagonal_set": record["terminal_diagonal_set"],
            "F_2110": record["F_2110"],
            "F_1111": record["F_1111"],
            "F_2200": record["F_2200"],
            "terminal_set_is_translation_subset": record[
                "terminal_set_is_translation_subset"
            ],
            "terminal_translation_offset_count": record[
                "terminal_translation_offset_count"
            ],
            "terminal_linear_part_counts": record["terminal_linear_part_counts"],
        }
        key = profile_key(profile)
        terminal_profile_counter[key] += 1
        terminal_profile_examples.setdefault(
            key, {"square_index": record["square_index"], "mask": record["mask"]}
        )

    f2110_by_terminal_class = {
        str(f2110): counter_json(
            Counter(record["terminal_set_class"] for record in rows)
        )
        for f2110, rows in sorted(by_f2110.items())
    }
    f2110_by_translation_subset = {
        str(f2110): counter_json(
            Counter(record["terminal_set_is_translation_subset"] for record in rows)
        )
        for f2110, rows in sorted(by_f2110.items())
    }
    terminal_profiles = [
        {
            "count": count,
            "profile": json.loads(key),
            "example": terminal_profile_examples[key],
        }
        for key, count in sorted(
            terminal_profile_counter.items(),
            key=lambda item: (json.loads(item[0])["F_2110"], item[0]),
        )
    ]

    f2110_12_iff_two_diagonal = all(
        (record["F_2110"] == 12)
        == (record["terminal_set_class"] == "two_diagonal_pair")
        for record in records
    )
    f2110_16_iff_v4_like = all(
        (record["F_2110"] == 16)
        == (record["terminal_set_class"] in {"v4_like_0213", "v4_like_1302"})
        for record in records
    )
    f2110_12_iff_translation_subset = all(
        (record["F_2110"] == 12)
        == record["terminal_set_is_translation_subset"]
        for record in records
    )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "P6",
            "description": "Linear quotient-shadow lemma and terminal-set explanation of the extra-32 F_2110 split.",
        },
        "quotient_shadow_lemma": {
            "spread_dimension": 2,
            "plane_dimension": 2,
            "possible_quotient_image_dimensions": [0, 1, 2],
            "allowed_sorted_shadows": ["4,0,0,0", "2,2,0,0", "1,1,1,1"],
            "forbidden_shadow": "2,1,1,0",
            "proof_sketch": (
                "If A is a 2-dimensional affine plane and W0 is the 2-dimensional "
                "translation spread direction, the projection pi(A) in V/W0 is an "
                "affine subspace of dimension r=0,1,2.  Each nonempty fiber of "
                "pi|A has size 2^(2-r), so the four coset counts are respectively "
                "4,0,0,0; 2,2,0,0; or 1,1,1,1 after sorting."
            ),
        },
        "extra32_count": len(records),
        "F_2110_distribution": counter_json(Counter(r["F_2110"] for r in records)),
        "F_2110_by_terminal_set_class": f2110_by_terminal_class,
        "F_2110_by_translation_subset": f2110_by_translation_subset,
        "terminal_profile_rows": terminal_profiles,
        "equivalences": {
            "F_2110_12_iff_two_diagonal_pair": f2110_12_iff_two_diagonal,
            "F_2110_16_iff_v4_like": f2110_16_iff_v4_like,
            "F_2110_12_iff_terminal_translation_subset": (
                f2110_12_iff_translation_subset
            ),
        },
    }


def write_report(result: dict, root: Path) -> None:
    lines = [
        "# Phase P6 Forbidden-Shadow Split",
        "",
        "## Quotient-Shadow Lemma",
        "",
        "For a domain-affine plane in `F2^4`, quotienting by the fixed",
        "translation spread direction gives an affine subspace of dimension",
        "`0`, `1`, or `2`.  Therefore the sorted block shadows are only:",
        "",
        "```text",
        "4,0,0,0",
        "2,2,0,0",
        "1,1,1,1",
        "```",
        "",
        "The profile `2,1,1,0` is forbidden because the nonempty quotient",
        "fibers of an affine plane all have equal size.",
        "",
        "## Extra-32 Split",
        "",
        "```text",
        f"extra32_count={result['extra32_count']}",
        f"F_2110_distribution={result['F_2110_distribution']}",
        f"F_2110_by_terminal_set_class={result['F_2110_by_terminal_set_class']}",
        f"F_2110_by_translation_subset={result['F_2110_by_translation_subset']}",
        "```",
        "",
        "Terminal profiles:",
        "",
        "```text",
    ]
    for row in result["terminal_profile_rows"]:
        profile = row["profile"]
        lines.append(
            "count={count} F2110={F} class={klass} set={words} "
            "translation_subset={subset} linear_parts={linear} example={example}".format(
                count=row["count"],
                F=profile["F_2110"],
                klass=profile["terminal_set_class"],
                words=",".join(profile["terminal_diagonal_set"]),
                subset=profile["terminal_set_is_translation_subset"],
                linear=profile["terminal_linear_part_counts"],
                example=row["example"],
            )
        )
    lines.extend(
        [
            "```",
            "",
            "Equivalences:",
            "",
            "```text",
            f"{result['equivalences']}",
            "```",
            "",
            "## Interpretation",
            "",
            "The `F_2110=12/16` split is not a new independent mystery.  It",
            "is exactly the terminal-set split already seen in the extra-32",
            "audit: the two-diagonal translation-subset records have",
            "`F_2110=12`, while the two v4-like terminal-set classes have",
            "`F_2110=16`.",
        ]
    )
    (root / "results" / "FORBIDDEN_SHADOW_SPLIT_P6_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = build_audit(root)
    if args.write:
        result_path = root / "results" / "forbidden_shadow_split_p6.json"
        result_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        write_report(result, root)
        print(result_path)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
