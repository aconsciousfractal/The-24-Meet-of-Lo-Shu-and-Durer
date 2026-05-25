"""Phase P: Johnson-scheme profiles for quaterne transport.

The quaternes are 4-subsets of the 16 cells.  A selected mask is also a
4-subset, so the first Johnson-scheme invariant is the intersection stratum
|Q cap M|.  This audit keeps the computation finite and lightweight:

- replay the Durer/Sagrada Johnson strata;
- record inner Johnson intersection distributions for source and terminal
  quaterne families;
- compare the same profiles across the terminal-24 atlas classes
  exact-V4 / selected-affine extras / outside-main.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


CellIndex = int
Quad = tuple[CellIndex, CellIndex, CellIndex, CellIndex]
Square = tuple[tuple[int, ...], ...]
Perm = tuple[int, int, int, int]


DURER_COMPLEMENT: Square = (
    (1, 14, 15, 4),
    (12, 7, 6, 9),
    (8, 11, 10, 5),
    (13, 2, 3, 16),
)

SAGRADA_MASK: Perm = (2, 0, 1, 3)


def cell_index(i: int, j: int) -> int:
    return 4 * i + j


def cell_from_index(idx: int) -> tuple[int, int]:
    return divmod(idx, 4)


def perm_from_string(text: str) -> Perm:
    return tuple(int(c) for c in text)  # type: ignore[return-value]


def mask_quad(mask: Perm) -> Quad:
    return tuple(sorted(cell_index(i, mask[i]) for i in range(4)))  # type: ignore[return-value]


def all_quads() -> tuple[Quad, ...]:
    return tuple(itertools.combinations(range(16), 4))  # type: ignore[return-value]


ALL_QUADS = all_quads()


def square_value(square: Square, idx: CellIndex) -> int:
    i, j = cell_from_index(idx)
    return square[i][j]


def quad_sum(square: Square, quad: Iterable[CellIndex]) -> int:
    return sum(square_value(square, idx) for idx in quad)


def quad_incidence(quad: Iterable[CellIndex], mask: Quad) -> int:
    return len(set(quad) & set(mask))


def is_value_affine_plane(square: Square, quad: Iterable[CellIndex]) -> bool:
    xor = 0
    for idx in quad:
        xor ^= square_value(square, idx) - 1
    return xor == 0


def counter_to_profile(counter: Counter[int], keys: Iterable[int]) -> dict[str, int]:
    return {str(k): counter.get(k, 0) for k in keys}


def dict_counter_to_sorted_dict(counter: Counter[tuple[int, int]]) -> dict[str, int]:
    return {f"source_{s}_incidence_{i}": counter[(s, i)] for s, i in sorted(counter)}


def johnson_stratum_profile(quads: Iterable[Quad], mask: Quad) -> dict[str, int]:
    counter = Counter(quad_incidence(q, mask) for q in quads)
    return counter_to_profile(counter, range(5))


def johnson_inner_intersection_profile(quads: Iterable[Quad]) -> dict[str, int]:
    """Unordered pair profile by |Q cap R|, including no diagonal pairs."""

    quads = tuple(quads)
    counter: Counter[int] = Counter()
    for a, b in itertools.combinations(quads, 2):
        counter[len(set(a) & set(b))] += 1
    return counter_to_profile(counter, range(5))


def profile_signature(profile: object) -> str:
    return json.dumps(profile, sort_keys=True, separators=(",", ":"))


def quaterne_profile(square: Square, mask_perm: Perm) -> dict:
    mask = mask_quad(mask_perm)
    values = [square_value(square, idx) for idx in mask]
    t_max = min(v - 1 for v in values)
    target = 34 - t_max

    source_h34: list[Quad] = []
    source_h34_affine: list[Quad] = []
    terminal: list[Quad] = []
    terminal_affine: list[Quad] = []
    terminal_decomp: Counter[tuple[int, int]] = Counter()
    terminal_affine_decomp: Counter[tuple[int, int]] = Counter()

    for quad in ALL_QUADS:
        source_sum = quad_sum(square, quad)
        incidence = quad_incidence(quad, mask)
        terminal_sum = source_sum - t_max * incidence
        affine = is_value_affine_plane(square, quad)
        if source_sum == 34:
            source_h34.append(quad)
            if affine:
                source_h34_affine.append(quad)
        if terminal_sum == target:
            terminal.append(quad)
            terminal_decomp[(source_sum, incidence)] += 1
            if affine:
                terminal_affine.append(quad)
                terminal_affine_decomp[(source_sum, incidence)] += 1

    return {
        "mask": "".join(str(x) for x in mask_perm),
        "mask_cells": list(mask),
        "selected_values": values,
        "t_max": t_max,
        "terminal_sum": target,
        "source_h34_count": len(source_h34),
        "source_h34_johnson_strata": johnson_stratum_profile(source_h34, mask),
        "source_h34_affine_count": len(source_h34_affine),
        "source_h34_affine_johnson_strata": johnson_stratum_profile(
            source_h34_affine, mask
        ),
        "source_h34_inner_profile": johnson_inner_intersection_profile(source_h34),
        "source_h34_affine_inner_profile": johnson_inner_intersection_profile(
            source_h34_affine
        ),
        "terminal_count": len(terminal),
        "terminal_johnson_strata": johnson_stratum_profile(terminal, mask),
        "terminal_decomposition": dict_counter_to_sorted_dict(terminal_decomp),
        "terminal_inner_profile": johnson_inner_intersection_profile(terminal),
        "terminal_affine_count": len(terminal_affine),
        "terminal_affine_johnson_strata": johnson_stratum_profile(
            terminal_affine, mask
        ),
        "terminal_affine_decomposition": dict_counter_to_sorted_dict(
            terminal_affine_decomp
        ),
        "terminal_affine_inner_profile": johnson_inner_intersection_profile(
            terminal_affine
        ),
    }


def load_essential_squares(root: Path) -> tuple[Square, ...]:
    data = json.loads((root / "data" / "order4_normal_essential_880.json").read_text())
    return tuple(tuple(tuple(row) for row in square) for square in data["essential_representatives"])


def load_terminal24_classes(root: Path) -> dict[tuple[int, str], str]:
    exact = json.loads(
        (root / "results" / "exact_v4_structural_characterization.json").read_text()
    )
    split = json.loads(
        (root / "results" / "inside_out_main_signature_split.json").read_text()
    )
    classes: dict[tuple[int, str], str] = {}
    for record in exact["records"]:
        key = (record["square_index"], record["mask"])
        classes[key] = "exact_v4" if record["exact_canonical_v4"] else "outside_main"
    for record in split["extra_records"]:
        classes[(record["square_index"], record["mask"])] = "extra32"
    return classes


def load_terminal24_pairs(root: Path) -> list[dict]:
    data = json.loads((root / "results" / "order4_terminal24_fingerprints.json").read_text())
    return data["records"]


def summarize_class_profiles(records: list[dict]) -> dict:
    by_class: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_class[record["class"]].append(record)

    signature_fields = [
        "source_h34_johnson_strata",
        "source_h34_affine_johnson_strata",
        "terminal_johnson_strata",
        "terminal_decomposition",
        "terminal_affine_johnson_strata",
        "terminal_affine_decomposition",
        "terminal_inner_profile",
        "terminal_affine_inner_profile",
    ]

    summary = {}
    for class_name, class_records in sorted(by_class.items()):
        field_summaries = {}
        for field in signature_fields:
            counts = Counter(profile_signature(r["profile"][field]) for r in class_records)
            field_summaries[field] = {
                "signature_count": len(counts),
                "top": [
                    {"count": count, "signature": json.loads(signature)}
                    for signature, count in counts.most_common(5)
                ],
            }
        combined_counts = Counter(
            profile_signature(
                {
                    field: r["profile"][field]
                    for field in (
                        "terminal_decomposition",
                        "terminal_affine_decomposition",
                        "terminal_inner_profile",
                        "terminal_affine_inner_profile",
                    )
                }
            )
            for r in class_records
        )
        summary[class_name] = {
            "record_count": len(class_records),
            "field_summaries": field_summaries,
            "combined_signature_count": len(combined_counts),
            "combined_top": [
                {"count": count, "signature": json.loads(signature)}
                for signature, count in combined_counts.most_common(5)
            ],
        }

    return summary


def signature_separation(records: list[dict], field: str) -> dict:
    classes = sorted({r["class"] for r in records})
    by_class = {
        c: {
            profile_signature(r["profile"][field])
            for r in records
            if r["class"] == c
        }
        for c in classes
    }
    intersections = {}
    for a, b in itertools.combinations(classes, 2):
        intersections[f"{a}__{b}"] = len(by_class[a] & by_class[b])
    return {
        "field": field,
        "signature_counts": {c: len(by_class[c]) for c in classes},
        "pairwise_intersections": intersections,
        "separates_main_176_from_outside_60": (
            intersections.get("exact_v4__outside_main", 1) == 0
            and intersections.get("extra32__outside_main", 1) == 0
        ),
        "separates_exact_144_from_extra_32": (
            intersections.get("exact_v4__extra32", 1) == 0
        ),
        "separates_all_classes": all(v == 0 for v in intersections.values()),
    }


def build_audit(root: Path) -> dict:
    squares = load_essential_squares(root)
    classes = load_terminal24_classes(root)
    terminal24_pairs = load_terminal24_pairs(root)

    atlas_records = []
    for pair in terminal24_pairs:
        key = (pair["square_index"], pair["mask"])
        class_name = classes[key]
        profile = quaterne_profile(squares[key[0]], perm_from_string(key[1]))
        atlas_records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "class": class_name,
                "profile": profile,
            }
        )

    separation_fields = [
        "source_h34_johnson_strata",
        "source_h34_affine_johnson_strata",
        "terminal_johnson_strata",
        "terminal_decomposition",
        "terminal_affine_johnson_strata",
        "terminal_affine_decomposition",
        "terminal_inner_profile",
        "terminal_affine_inner_profile",
    ]

    durer_profile = quaterne_profile(DURER_COMPLEMENT, SAGRADA_MASK)
    ambient_strata = {
        str(k): 1
        for k in range(5)
    }
    mask_size = 4
    outside = 12
    for k in range(5):
        if k <= mask_size and 4 - k <= outside:
            # C(4,k) C(12,4-k)
            ambient_strata[str(k)] = (
                len(tuple(itertools.combinations(range(mask_size), k)))
                * len(tuple(itertools.combinations(range(outside), 4 - k)))
            )
        else:
            ambient_strata[str(k)] = 0

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "P",
            "description": "Johnson-scheme quaterne transport profiles for Durer/Sagrada and the terminal-24 atlas.",
            "source_terminal24": "results/order4_terminal24_fingerprints.json",
            "source_classes": [
                "results/exact_v4_structural_characterization.json",
                "results/inside_out_main_signature_split.json",
            ],
        },
        "johnson_scheme": {
            "ambient": "J(16,4)",
            "stratum_definition": "J_i(M) = {Q: |Q cap M| = i}",
            "ambient_strata_for_fixed_mask": ambient_strata,
        },
        "durer_sagrada": durer_profile,
        "atlas_class_counts": dict(Counter(r["class"] for r in atlas_records)),
        "atlas_class_summary": summarize_class_profiles(atlas_records),
        "separation_tests": [
            signature_separation(atlas_records, field) for field in separation_fields
        ],
        "interpretation": {
            "johnson_transport_identity": "sum_{Q}(A-tM) = sum_{Q}(A) - t |Q cap M|",
            "main_positive_result": "The tested Johnson profiles separate the main 176-pair selected-affine signature from the 60 outside-main records.",
            "main_negative_result": "The tested Johnson profiles do not separate the 144 exact-V4 records from the 32 selected-affine extras.",
            "paper_role": "Useful notation and a classifier for 176 versus outside-main; not a conceptual solution of the 144/32 boundary.",
        },
        "sample_records": atlas_records[:5],
    }


def write_report(result: dict, root: Path) -> None:
    lines = [
        "# Phase P Johnson Quaterne Layer",
        "",
        "## Durer/Sagrada Replay",
        "",
        "```text",
        f"H34 Johnson strata: {result['durer_sagrada']['source_h34_johnson_strata']}",
        f"H34 affine strata: {result['durer_sagrada']['source_h34_affine_johnson_strata']}",
        f"Terminal decomposition: {result['durer_sagrada']['terminal_decomposition']}",
        f"Terminal affine decomposition: {result['durer_sagrada']['terminal_affine_decomposition']}",
        "```",
        "",
        "## Atlas Class Counts",
        "",
        "```text",
        json.dumps(result["atlas_class_counts"], sort_keys=True),
        "```",
        "",
        "## Separation Tests",
        "",
        "```text",
    ]
    for row in result["separation_tests"]:
        lines.append(
            f"{row['field']}: counts={row['signature_counts']} "
            f"intersections={row['pairwise_intersections']} "
            f"main_vs_outside={row['separates_main_176_from_outside_60']} "
            f"exact_vs_extra={row['separates_exact_144_from_extra_32']} "
            f"separates_all={row['separates_all_classes']}"
        )
    lines.extend(
        [
            "```",
            "",
            "## Interpretation",
            "",
            "The Johnson stratum identity cleanly explains quaterne transport by",
            "`|Q cap M|`.  The first atlas pass records whether these profiles",
            "separate the `144` exact class, the `32` selected-affine extras, and",
            "the remaining `60` outside-main records.  If a profile has nonzero",
            "pairwise intersections, it is useful language but not a classifier.",
            "",
            "Current result: the tested Johnson profiles separate the main",
            "`176 = 144 + 32` selected-affine signature from the `60` outside-main",
            "records, but they do not separate the `144` exact-`V4` records from",
            "the `32` selected-affine extras.",
            "",
        ]
    )
    (root / "results" / "JOHNSON_QUATERNE_LAYER_P_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    result = build_audit(root)
    if args.write:
        out = root / "results" / "johnson_quaterne_layer_p.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, root)
        print(out)
    else:
        summary = dict(result)
        summary["sample_records"] = f"{len(result['sample_records'])} samples omitted"
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
