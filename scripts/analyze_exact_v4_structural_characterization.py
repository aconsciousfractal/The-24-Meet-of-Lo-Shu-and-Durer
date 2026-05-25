"""Phase O structural characterization audit for the exact-V4 affine class."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import analyze_exact_v4_affine_mechanism as mechanism
import analyze_order4_f2_extension as f2ext


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def split_key(*parts: object) -> str:
    return " | ".join(str(part) for part in parts)


def build_exact_v4_structural_characterization() -> dict:
    root = Path(__file__).resolve().parents[1]
    dataset = f2ext.load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]
    records = f2ext.build_order4_f2_extension()["records"]

    exact_pairs = set()
    condition_pairs: dict[str, set[tuple[int, str]]] = {
        "cell_value_affine": set(),
        "selected_mask_affine": set(),
        "selected_values_11_12_15_16": set(),
        "full_translation_terminal_v4": set(),
        "translation_subset_terminal": set(),
        "zero_affine_defect": set(),
        "preserves_all_140_domain_affine_planes": set(),
        "preserves_all_24_permutation_diagonal_planes": set(),
        "terminal_count_96": set(),
        "terminal_affine_count_36": set(),
        "pure_terminal_affine_transport": set(),
    }

    defect_signature_counter = Counter()
    near_miss_counter = Counter()
    terminal_set_counter = Counter()
    records_brief = []

    for profile in records:
        pair = (profile["square_index"], profile["mask"])
        square = squares[profile["square_index"]]
        defect = mechanism.affine_defect_profile(square)
        terminal_profile = mechanism.terminal_set_profile(
            profile["terminal_diagonal_set"]
        )

        exact = profile["is_exact_canonical_v4"]
        selected_affine = profile["selected_mask_is_affine_plane"]
        selected_high = tuple(profile["sorted_values"]) == (11, 12, 15, 16)
        cell_affine = profile["cell_labeling"]["is_affine_automorphism"]
        full_translation = terminal_profile["is_full_translation_v4"]
        translation_subset = terminal_profile["is_translation_subset"]
        mismatch = defect["basis_interpolation_mismatch_count"]
        planes = defect["preserved_domain_affine_planes"]
        diagonals = defect["preserved_permutation_diagonal_planes"]
        terminal_count_96 = profile["terminal_f2_profile"]["terminal_count"] == 96
        terminal_affine_count_36 = (
            profile["terminal_f2_profile"]["terminal_affine_count"] == 36
        )
        pure_transport = profile["terminal_f2_profile"][
            "terminal_affine_is_pure_transport"
        ]

        if exact:
            exact_pairs.add(pair)
        if cell_affine:
            condition_pairs["cell_value_affine"].add(pair)
        if selected_affine:
            condition_pairs["selected_mask_affine"].add(pair)
        if selected_high:
            condition_pairs["selected_values_11_12_15_16"].add(pair)
        if full_translation:
            condition_pairs["full_translation_terminal_v4"].add(pair)
        if translation_subset:
            condition_pairs["translation_subset_terminal"].add(pair)
        if mismatch == 0:
            condition_pairs["zero_affine_defect"].add(pair)
        if planes == 140:
            condition_pairs["preserves_all_140_domain_affine_planes"].add(pair)
        if diagonals == 24:
            condition_pairs["preserves_all_24_permutation_diagonal_planes"].add(pair)
        if terminal_count_96:
            condition_pairs["terminal_count_96"].add(pair)
        if terminal_affine_count_36:
            condition_pairs["terminal_affine_count_36"].add(pair)
        if pure_transport:
            condition_pairs["pure_terminal_affine_transport"].add(pair)

        defect_key = split_key(
            "exact" if exact else "nonexact",
            f"selected_affine={selected_affine}",
            f"mismatch={mismatch}",
            f"planes={planes}",
            f"perm_diags={diagonals}",
        )
        defect_signature_counter[defect_key] += 1

        terminal_set_counter[
            ",".join(sorted(profile["terminal_diagonal_set"]))
        ] += 1

        if not exact:
            if selected_affine and mismatch == 4:
                near_miss = "selected_affine_defect4"
            elif (not selected_affine) and mismatch == 4:
                near_miss = "nonselected_defect4"
            elif (not selected_affine) and mismatch == 6:
                near_miss = "nonselected_defect6"
            else:
                near_miss = "other_nonexact"
            near_miss_counter[near_miss] += 1

        records_brief.append(
            {
                "square_index": profile["square_index"],
                "mask": profile["mask"],
                "exact_canonical_v4": exact,
                "cell_value_affine": cell_affine,
                "selected_mask_affine": selected_affine,
                "selected_values_11_12_15_16": selected_high,
                "terminal_set": sorted(profile["terminal_diagonal_set"]),
                "full_translation_terminal_v4": full_translation,
                "translation_subset_terminal": translation_subset,
                "basis_mismatch": mismatch,
                "preserved_domain_affine_planes": planes,
                "preserved_permutation_diagonal_planes": diagonals,
                "terminal_count": profile["terminal_f2_profile"]["terminal_count"],
                "terminal_affine_count": profile["terminal_f2_profile"][
                    "terminal_affine_count"
                ],
                "pure_terminal_affine_transport": pure_transport,
            }
        )

    exact_count = len(exact_pairs)
    condition_summary = {}
    exact_equivalent_conditions = []
    exact_implied_but_too_broad = []
    for name, pairs in condition_pairs.items():
        exact_intersection = len(pairs & exact_pairs)
        is_equivalent = pairs == exact_pairs
        condition_summary[name] = {
            "count": len(pairs),
            "contains_all_exact": exact_pairs <= pairs,
            "exact_intersection_count": exact_intersection,
            "false_positive_count": len(pairs - exact_pairs),
            "false_negative_count": len(exact_pairs - pairs),
            "equivalent_to_exact_v4": is_equivalent,
        }
        if is_equivalent:
            exact_equivalent_conditions.append(name)
        elif exact_pairs <= pairs:
            exact_implied_but_too_broad.append(name)

    composite_conditions = {
        "selected_mask_affine_and_cell_value_affine": (
            condition_pairs["selected_mask_affine"]
            & condition_pairs["cell_value_affine"]
        ),
        "selected_values_11_12_15_16_and_cell_value_affine": (
            condition_pairs["selected_values_11_12_15_16"]
            & condition_pairs["cell_value_affine"]
        ),
        "selected_mask_affine_and_full_translation_terminal_v4": (
            condition_pairs["selected_mask_affine"]
            & condition_pairs["full_translation_terminal_v4"]
        ),
        "terminal_affine_count_36_and_zero_affine_defect": (
            condition_pairs["terminal_affine_count_36"]
            & condition_pairs["zero_affine_defect"]
        ),
    }
    composite_summary = {}
    for name, pairs in composite_conditions.items():
        composite_summary[name] = {
            "count": len(pairs),
            "false_positive_count": len(pairs - exact_pairs),
            "false_negative_count": len(exact_pairs - pairs),
            "equivalent_to_exact_v4": pairs == exact_pairs,
        }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase O",
            "description": "Structural characterization audit for the 144-pair exact canonical V4 affine subclass.",
            "scope": "236 terminal-24 order-four square-mask records",
        },
        "terminal24_pair_count": len(records),
        "exact_canonical_v4_pair_count": exact_count,
        "exact_equivalent_single_conditions": sorted(exact_equivalent_conditions),
        "exact_implied_but_too_broad_single_conditions": sorted(
            exact_implied_but_too_broad
        ),
        "single_condition_summary": condition_summary,
        "composite_condition_summary": composite_summary,
        "defect_signature_counts": counter_json(defect_signature_counter),
        "nonexact_near_miss_classes": counter_json(near_miss_counter),
        "terminal_set_counts": counter_json(terminal_set_counter),
        "classification_reading": {
            "exact_v4_is_zero_defect_global_affine_class": (
                set(condition_pairs["zero_affine_defect"]) == exact_pairs
                and set(condition_pairs["cell_value_affine"]) == exact_pairs
            ),
            "exact_v4_is_full_translation_terminal_class": (
                set(condition_pairs["full_translation_terminal_v4"]) == exact_pairs
            ),
            "selected_mask_affine_is_broader_176_class": (
                len(condition_pairs["selected_mask_affine"]) == 176
            ),
            "selected_mask_affine_plus_zero_defect_is_exact_v4": (
                condition_pairs["selected_mask_affine"]
                & condition_pairs["zero_affine_defect"]
                == exact_pairs
            ),
        },
        "records": records_brief,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Exact-V4 Structural Characterization",
        "",
        "Status: Phase O finite structural characterization audit",
        "",
        "## Scope",
        "",
        "This audit works inside the `236` terminal-24 order-four",
        "square-mask records.  It asks which conditions are equivalent to",
        "the `144`-pair exact canonical `V4` subclass, and which conditions",
        "are only broader filters.",
        "",
        "## Equivalent Single Conditions",
        "",
    ]
    for name in result["exact_equivalent_single_conditions"]:
        lines.append(f"- `{name}`")
    lines.extend(
        [
            "",
            "Thus, within the terminal-24 atlas, the exact canonical `V4`",
            "class is equivalently:",
            "",
            "```text",
            "global affine cell-value class",
            "zero affine-defect class",
            "full translation terminal-V4 class",
            "class preserving all 140 domain affine planes",
            "class preserving all 24 permutation-diagonal affine planes",
            "```",
            "",
            "## Too-Broad Conditions",
            "",
        ]
    )
    for name in result["exact_implied_but_too_broad_single_conditions"]:
        summary = result["single_condition_summary"][name]
        lines.append(
            f"- `{name}`: count `{summary['count']}`, false positives `{summary['false_positive_count']}`"
        )
    lines.extend(
        [
            "",
            "The key broad filter is selected-mask affineness / selected values",
            "`{11,12,15,16}`.  It gives the `176`-pair main class, not the",
            "`144` exact-`V4` class.",
            "",
            "## Composite Checks",
            "",
        ]
    )
    for name, summary in result["composite_condition_summary"].items():
        lines.append(
            f"- `{name}`: count `{summary['count']}`, equivalent `{summary['equivalent_to_exact_v4']}`"
        )
    lines.extend(
        [
            "",
            "## Defect Stratification",
            "",
        ]
    )
    for key, count in result["defect_signature_counts"].items():
        lines.append(f"- `{key}`: `{count}`")
    lines.extend(
        [
            "",
            "## Nonexact Near Misses",
            "",
        ]
    )
    for key, count in result["nonexact_near_miss_classes"].items():
        lines.append(f"- `{key}`: `{count}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Phase O upgrades the Phase-J equality into a sharper finite",
            "characterization.  The `144` class is not merely the terminal",
            "word set `{0123,1032,2301,3210}`.  It is the zero-defect global",
            "affine class, equivalently the class whose terminal diagonal set",
            "is the full translation `V4` in the canonical `F2^2` model.",
            "",
            "The `32` selected-affine extras are the first near-miss layer:",
            "their selected mask is affine and their selected values are",
            "`{11,12,15,16}`, but they have affine defect `4` rather than `0`.",
            "",
            "## Guardrail",
            "",
            "This is still a finite characterization inside the `236`",
            "terminal-24 records.  It is not a theorem for all order-four",
            "endpoint classes and it does not explain the Lo Shu side of the",
            "meet.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_exact_v4_structural_characterization()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "exact_v4_structural_characterization.json"
        report_path = (
            root / "results" / "EXACT_V4_STRUCTURAL_CHARACTERIZATION_REPORT.md"
        )
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
