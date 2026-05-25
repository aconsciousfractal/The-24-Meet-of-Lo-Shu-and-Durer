"""Extend the F2^4 tesseract fingerprints across Phase-C terminal-24 pairs."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


Cell = tuple[int, int]
Mask = str

CANONICAL_V4 = tuple(sorted(("0123", "1032", "2301", "3210")))
CELL_BASIS = ((2, 0), (1, 0), (0, 2), (0, 1))


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def label_bits(label: int) -> tuple[int, int, int, int]:
    return tuple((label >> shift) & 1 for shift in (3, 2, 1, 0))  # type: ignore[return-value]


def gf2_rank_int(rows: Iterable[int]) -> int:
    rows = list(rows)
    rank = 0
    for bit in (8, 4, 2, 1):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] & bit), None)
        if pivot is not None:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            for i in range(len(rows)):
                if i != rank and rows[i] & bit:
                    rows[i] ^= rows[rank]
            rank += 1
    return rank


def all_cells() -> list[Cell]:
    return [(i, j) for i in range(4) for j in range(4)]


def mask_cells(mask: Mask) -> tuple[Cell, Cell, Cell, Cell]:
    return tuple((i, int(mask[i])) for i in range(4))  # type: ignore[return-value]


def square_label(square: list[list[int]], cell: Cell) -> int:
    i, j = cell
    return square[i][j] - 1


def square_value(square: list[list[int]], cell: Cell) -> int:
    i, j = cell
    return square[i][j]


def quad_xor_labels(labels: Iterable[int]) -> int:
    out = 0
    for label in labels:
        out ^= label
    return out


def is_label_affine_plane(labels: Iterable[int]) -> bool:
    labels_tuple = tuple(labels)
    return len(labels_tuple) == 4 and len(set(labels_tuple)) == 4 and quad_xor_labels(labels_tuple) == 0


def plane_direction(labels: Iterable[int]) -> tuple[int, int, int, int] | None:
    labels_tuple = tuple(labels)
    if not is_label_affine_plane(labels_tuple):
        return None
    base = labels_tuple[0]
    return tuple(sorted(base ^ label for label in labels_tuple))  # type: ignore[return-value]


def cell_labeling_affine_profile(square: list[list[int]]) -> dict:
    """Test whether cell -> value-1 is affine from F2^4 cell bits to value bits."""

    offset = square_label(square, (0, 0))
    columns = [square_label(square, cell) ^ offset for cell in CELL_BASIS]
    matches = True
    for i, j in all_cells():
        input_bits = ((i >> 1) & 1, i & 1, (j >> 1) & 1, j & 1)
        predicted = offset
        for bit, column in zip(input_bits, columns):
            if bit:
                predicted ^= column
        if predicted != square_label(square, (i, j)):
            matches = False
            break

    return {
        "is_affine": matches,
        "linear_rank_over_f2": gf2_rank_int(columns),
        "is_affine_automorphism": matches and gf2_rank_int(columns) == 4,
        "offset_label": offset,
        "linear_columns_as_labels": columns,
        "linear_columns_as_bits": [list(label_bits(column)) for column in columns],
    }


def source_sum_labels(labels: Iterable[int]) -> int:
    return sum(label + 1 for label in labels)


def label_space_terminal_profile(mask_labels: Iterable[int], t: int = 10) -> dict:
    mask_set = set(mask_labels)
    terminal_sets = []
    terminal_affine_sets = set()
    transported_affine_sets = set()
    terminal_split = Counter()

    for labels in itertools.combinations(range(16), 4):
        labels_set = set(labels)
        source_sum = source_sum_labels(labels)
        incidence = len(labels_set & mask_set)
        terminal_sum = source_sum - t * incidence
        affine = is_label_affine_plane(labels)
        if terminal_sum == 24:
            terminal_sets.append(labels)
            terminal_split[(source_sum, incidence, "affine" if affine else "non_affine")] += 1
            if affine:
                terminal_affine_sets.add(tuple(sorted(labels)))
        if source_sum == 34 and incidence == 1 and affine:
            transported_affine_sets.add(tuple(sorted(labels)))

    return {
        "terminal_count": len(terminal_sets),
        "terminal_affine_count": len(terminal_affine_sets),
        "transported_source34_incidence1_affine_count": len(transported_affine_sets),
        "terminal_affine_is_pure_transport": terminal_affine_sets == transported_affine_sets,
        "terminal_split": {
            f"source_{source}_incidence_{incidence}_{kind}": count
            for (source, incidence, kind), count in sorted(terminal_split.items())
        },
    }


def record_profile(record: dict, square: list[list[int]]) -> dict:
    selected_labels = [value - 1 for value in record["values"]]
    selected_direction = plane_direction(selected_labels)
    terminal_profile = label_space_terminal_profile(selected_labels, record["t_max"])
    cell_profile = cell_labeling_affine_profile(square)
    terminal_set = tuple(sorted(record["terminal_diagonal_set"]))

    return {
        "square_index": record["square_index"],
        "mask": record["mask"],
        "sorted_values": record["sorted_values"],
        "selected_labels": selected_labels,
        "selected_label_set": sorted(selected_labels),
        "selected_label_xor": quad_xor_labels(selected_labels),
        "selected_mask_is_affine_plane": selected_direction is not None,
        "selected_mask_direction": list(selected_direction) if selected_direction else None,
        "cell_labeling": cell_profile,
        "terminal_diagonal_set": record["terminal_diagonal_set"],
        "is_exact_canonical_v4": terminal_set == CANONICAL_V4,
        "terminal_f2_profile": terminal_profile,
    }


def counter_to_plain(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def signature_key(profile: dict) -> str:
    return ",".join(str(value) for value in profile["sorted_values"])


def build_order4_f2_extension() -> dict:
    root = Path(__file__).resolve().parents[1]
    dataset = load_json(root / "data" / "order4_normal_essential_880.json")
    terminal24 = load_json(root / "results" / "order4_terminal24_fingerprints.json")
    squares = dataset["essential_representatives"]  # type: ignore[index]
    records = terminal24["records"]  # type: ignore[index]

    profiles = [
        record_profile(record, squares[record["square_index"]])
        for record in records
    ]
    exact_v4_profiles = [profile for profile in profiles if profile["is_exact_canonical_v4"]]
    affine_cell_profiles = [
        profile for profile in profiles if profile["cell_labeling"]["is_affine_automorphism"]
    ]

    all_square_affine_counter = Counter()
    for square in squares:
        profile = cell_labeling_affine_profile(square)
        key = "affine_automorphism" if profile["is_affine_automorphism"] else "non_affine"
        all_square_affine_counter[key] += 1

    signature_profiles = Counter()
    for profile in profiles:
        f2 = profile["terminal_f2_profile"]
        signature_profiles[
            (
                signature_key(profile),
                profile["selected_mask_is_affine_plane"],
                f2["terminal_count"],
                f2["terminal_affine_count"],
                f2["transported_source34_incidence1_affine_count"],
                f2["terminal_affine_is_pure_transport"],
            )
        ] += 1

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase F extension",
            "description": "F2^4 fingerprints across the 236 terminal-24 Phase-C square-mask pairs.",
            "cell_model": "For each normal order-4 square Q, label a cell by Q[i,j]-1 in F2^4.",
        },
        "all_880_square_cell_labeling_affine_counts": counter_to_plain(all_square_affine_counter),
        "terminal24_pair_count": len(profiles),
        "exact_canonical_v4_pair_count": len(exact_v4_profiles),
        "terminal24_affine_cell_labeling_pair_count": len(affine_cell_profiles),
        "affine_cell_labeling_pairs_equal_exact_canonical_v4": {
            (profile["square_index"], profile["mask"]) for profile in affine_cell_profiles
        }
        == {
            (profile["square_index"], profile["mask"]) for profile in exact_v4_profiles
        },
        "selected_mask_affine_counts": counter_to_plain(
            Counter(
                "affine_plane" if profile["selected_mask_is_affine_plane"] else "non_affine"
                for profile in profiles
            )
        ),
        "selected_mask_direction_counts": counter_to_plain(
            Counter(
                tuple(profile["selected_mask_direction"])
                for profile in profiles
                if profile["selected_mask_direction"] is not None
            )
        ),
        "terminal_affine_pure_transport_counts": counter_to_plain(
            Counter(
                profile["terminal_f2_profile"]["terminal_affine_is_pure_transport"]
                for profile in profiles
            )
        ),
        "selected_value_signature_f2_profiles": [
            {
                "sorted_values": key[0],
                "selected_mask_is_affine_plane": key[1],
                "terminal_count": key[2],
                "terminal_affine_count": key[3],
                "transported_source34_incidence1_affine_count": key[4],
                "terminal_affine_is_pure_transport": key[5],
                "pair_count": count,
            }
            for key, count in sorted(signature_profiles.items(), key=lambda item: item[0])
        ],
        "exact_canonical_v4_summary": {
            "pair_count": len(exact_v4_profiles),
            "all_cell_labelings_are_affine_automorphisms": all(
                profile["cell_labeling"]["is_affine_automorphism"]
                for profile in exact_v4_profiles
            ),
            "all_selected_masks_are_affine_planes": all(
                profile["selected_mask_is_affine_plane"]
                for profile in exact_v4_profiles
            ),
            "selected_mask_direction_counts": counter_to_plain(
                Counter(tuple(profile["selected_mask_direction"]) for profile in exact_v4_profiles)
            ),
            "all_terminal_affine_layers_are_pure_transport": all(
                profile["terminal_f2_profile"]["terminal_affine_is_pure_transport"]
                for profile in exact_v4_profiles
            ),
            "terminal_affine_count_distribution": counter_to_plain(
                Counter(
                    profile["terminal_f2_profile"]["terminal_affine_count"]
                    for profile in exact_v4_profiles
                )
            ),
            "transported_affine_count_distribution": counter_to_plain(
                Counter(
                    profile["terminal_f2_profile"][
                        "transported_source34_incidence1_affine_count"
                    ]
                    for profile in exact_v4_profiles
                )
            ),
        },
        "records": profiles,
    }


def write_report(result: dict, path: Path) -> None:
    v4 = result["exact_canonical_v4_summary"]
    lines = [
        "# Order-4 F2 Extension Report",
        "",
        "Status: Phase F extension across terminal-24 Phase-C records",
        "",
        "## Summary",
        "",
        f"- all 880 cell-value affine counts: `{result['all_880_square_cell_labeling_affine_counts']}`",
        f"- terminal-24 pairs: `{result['terminal24_pair_count']}`",
        f"- exact canonical `V4` pairs: `{result['exact_canonical_v4_pair_count']}`",
        f"- terminal-24 pairs with affine cell-value labeling: `{result['terminal24_affine_cell_labeling_pair_count']}`",
        f"- affine cell-value labeling pairs equal exact canonical `V4`: `{result['affine_cell_labeling_pairs_equal_exact_canonical_v4']}`",
        f"- selected mask affine counts: `{result['selected_mask_affine_counts']}`",
        f"- selected mask direction counts: `{result['selected_mask_direction_counts']}`",
        f"- terminal affine pure-transport counts: `{result['terminal_affine_pure_transport_counts']}`",
        "",
        "## Exact Canonical V4 Subclass",
        "",
        f"- pair count: `{v4['pair_count']}`",
        f"- all cell labelings affine automorphisms: `{v4['all_cell_labelings_are_affine_automorphisms']}`",
        f"- all selected masks affine planes: `{v4['all_selected_masks_are_affine_planes']}`",
        f"- selected mask directions: `{v4['selected_mask_direction_counts']}`",
        f"- all terminal affine layers pure transport: `{v4['all_terminal_affine_layers_are_pure_transport']}`",
        f"- terminal affine count distribution: `{v4['terminal_affine_count_distribution']}`",
        f"- transported affine count distribution: `{v4['transported_affine_count_distribution']}`",
        "",
        "## Signature Profiles",
        "",
    ]
    for row in result["selected_value_signature_f2_profiles"]:
        lines.append(
            "- values `{sorted_values}`: count `{pair_count}`, mask affine `{selected_mask_is_affine_plane}`, "
            "terminal affine `{terminal_affine_count}`, transported affine `{transported_source34_incidence1_affine_count}`, "
            "pure `{terminal_affine_is_pure_transport}`".format(**row)
        )
    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "The exact canonical `V4` subclass is strongly aligned with affine",
            "cell-value labelings in this fixed orientation.  This is a finite",
            "Phase-C fingerprint, not a uniqueness theorem for endpoint `24` in all",
            "magic-square categories.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_order4_f2_extension()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "order4_f2_extension.json"
        report_path = root / "results" / "ORDER4_F2_EXTENSION_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "terminal24_pair_count": result["terminal24_pair_count"],
            "exact_canonical_v4_pair_count": result["exact_canonical_v4_pair_count"],
            "affine_cell_labeling_pairs_equal_exact_canonical_v4": result[
                "affine_cell_labeling_pairs_equal_exact_canonical_v4"
            ],
            "selected_mask_affine_counts": result["selected_mask_affine_counts"],
            "exact_canonical_v4_summary": result["exact_canonical_v4_summary"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
