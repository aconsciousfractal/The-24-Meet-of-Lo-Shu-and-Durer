"""Phase-F controls for F2^4 fingerprints on named order-4 families."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import analyze_order4_f2_extension as f2
import analyze_order4_named_families as families
import enumerate_order4_endpoints as order4


CONTROL_FAMILIES = (
    "associated",
    "complement_fixed",
    "panmagic",
    "local_2x2",
    "wrap_2x2",
    "most_perfect_proxy",
)


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def build_family_flags() -> tuple[list[order4.Square], list[dict[str, bool]]]:
    squares = order4.essential_order4_representatives()
    index_by_square = {square: idx for idx, square in enumerate(squares)}
    flags = [
        families.family_flags(square, index_by_square, idx)
        for idx, square in enumerate(squares)
    ]
    return squares, flags


def square_affine_profile(square: order4.Square) -> dict:
    return f2.cell_labeling_affine_profile([list(row) for row in square])


def summarize_family(
    name: str,
    squares: list[order4.Square],
    flags: list[dict[str, bool]],
    terminal_profiles: list[dict],
) -> dict:
    square_indices = [idx for idx, row in enumerate(flags) if row[name]]
    affine_square_indices = [
        idx
        for idx in square_indices
        if square_affine_profile(squares[idx])["is_affine_automorphism"]
    ]
    family_profiles = [
        profile for profile in terminal_profiles if flags[profile["square_index"]][name]
    ]

    return {
        "square_count": len(square_indices),
        "affine_cell_labeling_square_count": len(affine_square_indices),
        "affine_cell_labeling_square_fraction": f"{len(affine_square_indices)}/{len(square_indices)}",
        "terminal24_pair_count": len(family_profiles),
        "terminal24_affine_cell_labeling_pair_count": sum(
            1
            for profile in family_profiles
            if profile["cell_labeling"]["is_affine_automorphism"]
        ),
        "terminal24_selected_mask_affine_pair_count": sum(
            1 for profile in family_profiles if profile["selected_mask_is_affine_plane"]
        ),
        "terminal24_exact_canonical_v4_pair_count": sum(
            1 for profile in family_profiles if profile["is_exact_canonical_v4"]
        ),
        "terminal24_pure_transport_pair_count": sum(
            1
            for profile in family_profiles
            if profile["terminal_f2_profile"]["terminal_affine_is_pure_transport"]
        ),
        "terminal_affine_count_distribution": counter_json(
            Counter(
                profile["terminal_f2_profile"]["terminal_affine_count"]
                for profile in family_profiles
            )
        ),
        "selected_value_signature_counts": counter_json(
            Counter(tuple(profile["sorted_values"]) for profile in family_profiles)
        ),
        "selected_mask_direction_counts": counter_json(
            Counter(
                tuple(profile["selected_mask_direction"])
                for profile in family_profiles
                if profile["selected_mask_direction"] is not None
            )
        ),
        "square_indices": square_indices,
        "affine_cell_labeling_square_indices": affine_square_indices,
    }


def build_f2_family_controls() -> dict:
    squares, flags = build_family_flags()
    f2_extension = f2.build_order4_f2_extension()
    terminal_profiles = f2_extension["records"]
    summaries = {
        name: summarize_family(name, squares, flags, terminal_profiles)
        for name in CONTROL_FAMILIES
    }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase F family controls",
            "description": "F2^4 fingerprint controls on associated/complement-fixed and panmagic/most-perfect-proxy families.",
        },
        "family_summaries": summaries,
        "associated_vs_panmagic_control": {
            "associated_terminal24_profile": {
                key: summaries["associated"][key]
                for key in (
                    "terminal24_pair_count",
                    "terminal24_affine_cell_labeling_pair_count",
                    "terminal24_selected_mask_affine_pair_count",
                    "terminal24_exact_canonical_v4_pair_count",
                    "terminal24_pure_transport_pair_count",
                    "terminal_affine_count_distribution",
                    "selected_value_signature_counts",
                )
            },
            "most_perfect_proxy_terminal24_profile": {
                key: summaries["most_perfect_proxy"][key]
                for key in (
                    "terminal24_pair_count",
                    "terminal24_affine_cell_labeling_pair_count",
                    "terminal24_selected_mask_affine_pair_count",
                    "terminal24_exact_canonical_v4_pair_count",
                    "terminal24_pure_transport_pair_count",
                    "terminal_affine_count_distribution",
                    "selected_value_signature_counts",
                )
            },
            "same_terminal24_f2_profile": (
                summaries["associated"]["terminal24_pair_count"]
                == summaries["most_perfect_proxy"]["terminal24_pair_count"]
                == 16
                and summaries["associated"]["terminal24_affine_cell_labeling_pair_count"]
                == summaries["most_perfect_proxy"][
                    "terminal24_affine_cell_labeling_pair_count"
                ]
                == 16
                and summaries["associated"]["terminal_affine_count_distribution"]
                == summaries["most_perfect_proxy"]["terminal_affine_count_distribution"]
                == {"36": 16}
            ),
        },
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# F2 Family Control Report",
        "",
        "Status: Phase F control-branch audit",
        "",
        "## Summary",
        "",
    ]
    for name, summary in result["family_summaries"].items():
        lines.extend(
            [
                f"### {name}",
                "",
                f"- squares: `{summary['square_count']}`",
                f"- affine cell-labeling squares: `{summary['affine_cell_labeling_square_fraction']}`",
                f"- terminal-24 pairs: `{summary['terminal24_pair_count']}`",
                f"- terminal-24 affine cell-labeling pairs: `{summary['terminal24_affine_cell_labeling_pair_count']}`",
                f"- terminal-24 selected-mask affine pairs: `{summary['terminal24_selected_mask_affine_pair_count']}`",
                f"- exact canonical `V4` terminal pairs: `{summary['terminal24_exact_canonical_v4_pair_count']}`",
                f"- pure transport terminal pairs: `{summary['terminal24_pure_transport_pair_count']}`",
                f"- terminal affine count distribution: `{summary['terminal_affine_count_distribution']}`",
                f"- selected value signatures: `{summary['selected_value_signature_counts']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation",
            "",
            "The associated branch and the panmagic/most-perfect-proxy branch have",
            "the same terminal-24 `F2^4` profile at this resolution: each has 16",
            "terminal-24 pairs, all affine cell-labeling, all selected-mask affine,",
            "all exact canonical `V4`, all pure transport, and terminal affine",
            "count `36`.",
            "",
            "Thus the `F2^4` fingerprint confirms the exact-`V4` structure, but it",
            "does not separate the associated Durer/Sagrada branch from the",
            "panmagic/most-perfect-proxy control branch.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_f2_family_controls()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "f2_family_controls.json"
        report_path = root / "results" / "F2_FAMILY_CONTROL_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "associated": result["family_summaries"]["associated"],
            "most_perfect_proxy": result["family_summaries"]["most_perfect_proxy"],
            "same_terminal24_f2_profile": result["associated_vs_panmagic_control"][
                "same_terminal24_f2_profile"
            ],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
