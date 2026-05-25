"""Phase K1 audit for the 32 selected-mask-affine extras.

This audit is intentionally small.  It does not rerun the whole project
suite and it does not attempt a complete Markov or Hilbert theorem.  It
crosses the post-J2 affine-defect data with three lightweight invariants:

* the exact support of the four affine-interpolation mismatches,
* the first small-move Markov graph component/degree data,
* the finite Hilbert-style decomposition records already written in Phase H.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import analyze_exact_v4_affine_mechanism as j2
import analyze_terminal24_markov_graph as markov


PairKey = tuple[int, str]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def pair_key(record: dict) -> PairKey:
    return (int(record["square_index"]), str(record["mask"]))


def cell_name(index: int) -> str:
    row, col = j2.input_index_to_cell(index)
    return f"r{row}c{col}"


def affine_mismatch_indices(square: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    labels = j2.square_label_map(square)
    offset = labels[0]
    columns = [labels[index] ^ offset for index in (8, 4, 2, 1)]
    mismatches = []
    for index, actual in enumerate(labels):
        predicted = offset
        for bit, column in zip((8, 4, 2, 1), columns):
            if index & bit:
                predicted ^= column
        if predicted != actual:
            mismatches.append(index)
    return tuple(mismatches)


def mask_index_set(mask_text: str) -> set[int]:
    return set(j2.mask_indices(mask_text))


def build_markov_details() -> dict[PairKey, dict]:
    """Rebuild per-node details for the existing small-move graph."""

    root = Path(__file__).resolve().parents[1]
    terminal24 = load_json(root / "results" / "order4_terminal24_fingerprints.json")
    inside_out = load_json(root / "results" / "order4_inside_out_profiles.json")
    inside_by_pair = {
        pair_key(record): record
        for record in inside_out["records"]
    }
    squares = markov.order4.essential_order4_representatives()

    nodes = []
    for record in terminal24["records"]:
        key = pair_key(record)
        inside_record = inside_by_pair[key]
        nodes.append(
            {
                "key": key,
                "class": markov.node_class(inside_record),
                "terminal_flat": markov.terminal_flat(
                    squares[record["square_index"]], record["mask"], record["t_max"]
                ),
            }
        )

    signed_moves = set(markov.primitive_pm1_kernel_moves())
    signed_moves |= {tuple(-entry for entry in move) for move in signed_moves}
    index_by_flat = {node["terminal_flat"]: idx for idx, node in enumerate(nodes)}
    adjacency = [set() for _ in nodes]
    for idx, node in enumerate(nodes):
        flat = node["terminal_flat"]
        for move in signed_moves:
            neighbor_flat = tuple(flat[pos] + move[pos] for pos in range(16))
            neighbor = index_by_flat.get(neighbor_flat)
            if neighbor is None or idx >= neighbor:
                continue
            adjacency[idx].add(neighbor)
            adjacency[neighbor].add(idx)

    components = markov.connected_components(adjacency)
    component_by_node = {}
    for comp_id, comp in enumerate(components):
        class_counts = Counter(nodes[index]["class"] for index in comp)
        profile = ",".join(f"{name}:{class_counts[name]}" for name in sorted(class_counts))
        for index in comp:
            component_by_node[index] = {
                "component_id": comp_id,
                "component_size": len(comp),
                "component_profile": profile,
            }

    out = {}
    for index, node in enumerate(nodes):
        neighbor_classes = Counter(nodes[n]["class"] for n in adjacency[index])
        out[node["key"]] = {
            "degree": len(adjacency[index]),
            "neighbor_class_counts": counter_json(neighbor_classes),
            **component_by_node[index],
        }
    return out


def build_extra32_post_j2_audit() -> dict:
    root = Path(__file__).resolve().parents[1]
    dataset = load_json(root / "data" / "order4_normal_essential_880.json")
    squares = [
        tuple(tuple(row) for row in square)
        for square in dataset["essential_representatives"]
    ]

    split = load_json(root / "results" / "inside_out_main_signature_split.json")
    automorphism = load_json(root / "results" / "extra32_set_system_automorphisms.json")
    hilbert = load_json(root / "results" / "hilbert_semigroup_audit.json")

    extras = sorted(split["extra_records"], key=lambda rec: (rec["square_index"], rec["mask"]))
    auto_by_pair = {pair_key(record): record for record in automorphism["records"]}
    hilbert_by_pair = {pair_key(record): record for record in hilbert["terminal24_records"]}
    markov_by_pair = build_markov_details()

    records = []
    for record in extras:
        key = pair_key(record)
        square = squares[record["square_index"]]
        mismatch_indices = affine_mismatch_indices(square)
        mismatch_set = set(mismatch_indices)
        mask_set = mask_index_set(record["mask"])
        auto_record = auto_by_pair[key]
        hilbert_record = hilbert_by_pair[key]
        hilbert_decomposition = hilbert_record["decomposition"]
        markov_record = markov_by_pair[key]

        records.append(
            {
                "square_index": key[0],
                "mask": key[1],
                "terminal_set_class": auto_record["terminal_set_class"],
                "terminal_diagonal_set": record["terminal_diagonal_set"],
                "source_diagonal_size": auto_record["source_diagonal_size"],
                "complement_fixed": auto_record["family_flags"]["complement_fixed"],
                "apd_vector": record["apd_vector"],
                "mismatch_indices": list(mismatch_indices),
                "mismatch_cells": [cell_name(index) for index in mismatch_indices],
                "mismatch_mask_intersection_count": len(mismatch_set & mask_set),
                "mismatch_support_is_mask": mismatch_set == mask_set,
                "hilbert_min_atom_count": hilbert_decomposition["min_atom_count"],
                "hilbert_support_size": hilbert_decomposition["support_size"],
                "hilbert_atom_degree_profile": hilbert_decomposition[
                    "atom_magic_sum_coefficient_counts"
                ],
                "markov_degree": markov_record["degree"],
                "markov_neighbor_class_counts": markov_record["neighbor_class_counts"],
                "markov_component_size": markov_record["component_size"],
                "markov_component_profile": markov_record["component_profile"],
            }
        )

    by_terminal_class: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_terminal_class[record["terminal_set_class"]].append(record)

    summaries = {}
    for class_name, rows in sorted(by_terminal_class.items()):
        summaries[class_name] = {
            "count": len(rows),
            "source_diagonal_size_distribution": counter_json(
                Counter(row["source_diagonal_size"] for row in rows)
            ),
            "complement_fixed_distribution": counter_json(
                Counter(row["complement_fixed"] for row in rows)
            ),
            "mismatch_support_distribution": counter_json(
                Counter(tuple(row["mismatch_cells"]) for row in rows)
            ),
            "mismatch_mask_intersection_distribution": counter_json(
                Counter(row["mismatch_mask_intersection_count"] for row in rows)
            ),
            "hilbert_min_atom_count_distribution": counter_json(
                Counter(row["hilbert_min_atom_count"] for row in rows)
            ),
            "hilbert_support_size_distribution": counter_json(
                Counter(row["hilbert_support_size"] for row in rows)
            ),
            "markov_degree_distribution": counter_json(
                Counter(row["markov_degree"] for row in rows)
            ),
            "markov_component_profile_distribution": counter_json(
                Counter(row["markov_component_profile"] for row in rows)
            ),
        }

    global_summary = {
        "extra_pair_count": len(records),
        "terminal_set_class_distribution": counter_json(
            Counter(record["terminal_set_class"] for record in records)
        ),
        "mismatch_support_distribution": counter_json(
            Counter(tuple(record["mismatch_cells"]) for record in records)
        ),
        "mismatch_mask_intersection_distribution": counter_json(
            Counter(record["mismatch_mask_intersection_count"] for record in records)
        ),
        "mismatch_support_is_mask_count": sum(
            1 for record in records if record["mismatch_support_is_mask"]
        ),
        "hilbert_min_atom_count_distribution": counter_json(
            Counter(record["hilbert_min_atom_count"] for record in records)
        ),
        "markov_degree_distribution": counter_json(
            Counter(record["markov_degree"] for record in records)
        ),
        "markov_component_profile_distribution": counter_json(
            Counter(record["markov_component_profile"] for record in records)
        ),
    }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase K1",
            "description": "Post-J2 audit of the 32 selected-mask-affine extras using affine-defect support, small-move Markov data, and finite Hilbert-style decomposition data.",
            "guardrail": "This is a targeted invariant audit for the 32 extras; it is not a complete Markov-basis or Hilbert-basis theorem.",
        },
        "summary": global_summary,
        "terminal_class_summaries": summaries,
        "records": records,
    }


def write_report(result: dict, path: Path) -> None:
    summary = result["summary"]
    lines = [
        "# Extra-32 Post-J2 Audit",
        "",
        "Status: Phase K1 targeted invariant audit",
        "",
        "## Scope",
        "",
        "This audit focuses only on the `32` selected-mask-affine extras left",
        "after the Phase J2 mechanism audit.  It crosses three targeted",
        "invariants: affine-interpolation mismatch support, the existing",
        "small-move Markov graph, and the finite Hilbert-style decompositions.",
        "",
        "It deliberately does not rerun the full project suite.",
        "",
        "## Summary",
        "",
        f"- extra pairs: `{summary['extra_pair_count']}`",
        f"- terminal-set class distribution: `{summary['terminal_set_class_distribution']}`",
        f"- affine mismatch support distribution: `{summary['mismatch_support_distribution']}`",
        f"- mismatch/mask intersection distribution: `{summary['mismatch_mask_intersection_distribution']}`",
        f"- mismatch support equals selected mask: `{summary['mismatch_support_is_mask_count']}`",
        f"- Hilbert min atom-count distribution: `{summary['hilbert_min_atom_count_distribution']}`",
        f"- Markov degree distribution: `{summary['markov_degree_distribution']}`",
        f"- Markov component profiles: `{summary['markov_component_profile_distribution']}`",
        "",
        "## By Terminal-Set Class",
        "",
    ]
    for class_name, data in result["terminal_class_summaries"].items():
        lines.extend(
            [
                f"### {class_name}",
                "",
                f"- count: `{data['count']}`",
                f"- source diagonal size distribution: `{data['source_diagonal_size_distribution']}`",
                f"- complement-fixed distribution: `{data['complement_fixed_distribution']}`",
                f"- mismatch support distribution: `{data['mismatch_support_distribution']}`",
                f"- mismatch/mask intersection distribution: `{data['mismatch_mask_intersection_distribution']}`",
                f"- Hilbert min atom-count distribution: `{data['hilbert_min_atom_count_distribution']}`",
                f"- Hilbert support-size distribution: `{data['hilbert_support_size_distribution']}`",
                f"- Markov degree distribution: `{data['markov_degree_distribution']}`",
                f"- Markov component profiles: `{data['markov_component_profile_distribution']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Reading",
            "",
            "The three tested invariants refine the extras but do not collapse them",
            "to a single conceptual family.  The affine defect is uniform in size",
            "but not in support; the Markov graph separates isolated, paired, and",
            "mixed-component cases; the finite Hilbert profiles split the extras",
            "further without matching the terminal-set classes exactly.",
            "",
            "This supports the Phase K stop rule: unless a stronger invariant is",
            "found, the `32` extras should remain a controlled frontier rather",
            "than being promoted to a central theorem.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_extra32_post_j2_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "extra32_post_j2_audit.json"
        report_path = root / "results" / "EXTRA32_POST_J2_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        print(json.dumps(result["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
