"""Automorphism/source audit for the 32 extra main-signature records."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import networkx as nx

import analyze_inside_out_main_signature_split as main_split
import enumerate_order4_endpoints as order4


Cell = tuple[int, int]
Edge = tuple[Cell, ...]
Square = list[list[int]]
Mask = tuple[int, int, int, int]


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def all_cells() -> list[Cell]:
    return [(i, j) for i in range(4) for j in range(4)]


def normalize_edge(cells: Iterable[Cell]) -> Edge:
    return tuple(sorted(cells))


def perm_from_string(text: str) -> Mask:
    return tuple(int(c) for c in text)  # type: ignore[return-value]


def cell_label(cell: Cell) -> str:
    return f"r{cell[0]}c{cell[1]}"


def row_edge(i: int) -> Edge:
    return normalize_edge((i, j) for j in range(4))


def col_edge(j: int) -> Edge:
    return normalize_edge((i, j) for i in range(4))


def main_diag_edge() -> Edge:
    return normalize_edge((i, i) for i in range(4))


def anti_diag_edge() -> Edge:
    return normalize_edge((i, 3 - i) for i in range(4))


def mask_edge(mask: Mask) -> Edge:
    return normalize_edge((i, mask[i]) for i in range(4))


def source_sum(square: Square, edge: Edge) -> int:
    return sum(square[i][j] for i, j in edge)


def mask_incidence(edge: Edge, mask: Mask) -> int:
    return sum(1 for i, j in edge if mask[i] == j)


def terminal_sum(square: Square, mask: Mask, edge: Edge, t: int) -> int:
    return source_sum(square, edge) - t * mask_incidence(edge, mask)


def base_records() -> list[dict]:
    records = []
    for i in range(4):
        records.append({"name": f"row_{i}", "color": "row", "edge": row_edge(i)})
    for j in range(4):
        records.append({"name": f"col_{j}", "color": "col", "edge": col_edge(j)})
    records.append({"name": "diag_main", "color": "diag_main", "edge": main_diag_edge()})
    records.append({"name": "diag_anti", "color": "diag_anti", "edge": anti_diag_edge()})
    return records


def h34_edges(square: Square) -> list[Edge]:
    return [
        normalize_edge(edge)
        for edge in itertools.combinations(all_cells(), 4)
        if source_sum(square, normalize_edge(edge)) == 34
    ]


def h24_edges(square: Square, mask: Mask, t: int) -> list[Edge]:
    return [
        normalize_edge(edge)
        for edge in itertools.combinations(all_cells(), 4)
        if terminal_sum(square, mask, normalize_edge(edge), t) == 24
    ]


def records_for_system(square: Square, mask: Mask, t: int, system: str) -> list[dict]:
    records = base_records()
    if system in {"lines_plus_mask", "source", "terminal", "combined"}:
        records.append({"name": "selected_mask", "color": "mask", "edge": mask_edge(mask)})
    if system in {"source", "combined"}:
        for idx, edge in enumerate(h34_edges(square)):
            records.append(
                {
                    "name": f"h34_{idx}",
                    "color": f"h34_incidence_{mask_incidence(edge, mask)}",
                    "edge": edge,
                }
            )
    if system in {"terminal", "combined"}:
        for idx, edge in enumerate(h24_edges(square, mask, t)):
            incidence = mask_incidence(edge, mask)
            records.append(
                {
                    "name": f"h24_{idx}",
                    "color": f"h24_source_{source_sum(square, edge)}_incidence_{incidence}",
                    "edge": edge,
                }
            )
    return records


def build_incidence_graph(records: list[dict]) -> nx.Graph:
    graph = nx.Graph()
    for cell in all_cells():
        graph.add_node(("cell", cell), kind="cell", color="cell")
    for idx, record in enumerate(records):
        edge_node = ("edge", idx)
        graph.add_node(edge_node, kind="edge", color=record["color"])
        for cell in record["edge"]:
            graph.add_edge(("cell", cell), edge_node)
    return graph


def cell_automorphisms(records: list[dict]) -> list[tuple[Cell, ...]]:
    graph = build_incidence_graph(records)

    def node_match(left: dict, right: dict) -> bool:
        return left["kind"] == right["kind"] and left["color"] == right["color"]

    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph, node_match=node_match)
    perms = {
        tuple(morphism[("cell", cell)][1] for cell in all_cells())
        for morphism in matcher.isomorphisms_iter()
    }
    return sorted(perms)


def automorphism_order(square: Square, mask: Mask, t: int, system: str) -> int:
    return len(cell_automorphisms(records_for_system(square, mask, t, system)))


def terminal_set_class(record: dict) -> str:
    terminal_set = record["terminal_diagonal_set"]
    if terminal_set == ["0123", "3210"]:
        return "two_diagonal_pair"
    if terminal_set == ["0123", "0213", "3120", "3210"]:
        return "v4_like_0213"
    if terminal_set == ["0123", "1302", "2031", "3210"]:
        return "v4_like_1302"
    return "other"


@lru_cache(maxsize=1)
def build_extra32_automorphism_audit() -> dict:
    split = main_split.build_main_signature_split()
    squares = order4.essential_order4_representatives()
    records = []
    system_tuple_counts = Counter()
    by_terminal_class: dict[str, list[dict]] = defaultdict(list)

    for record in split["extra_records"]:
        square = [list(row) for row in squares[record["square_index"]]]
        mask = perm_from_string(record["mask"])
        t = record.get("t_max", 10)
        aut_orders = {
            system: automorphism_order(square, mask, t, system)
            for system in ("lines_plus_mask", "source", "terminal", "combined")
        }
        enriched = {
            "square_index": record["square_index"],
            "mask": record["mask"],
            "terminal_set": record["terminal_diagonal_set"],
            "terminal_set_class": terminal_set_class(record),
            "terminal_order_profile": record["terminal_diagonal_order_profile"],
            "source_diagonal_size": len(record["source_diagonal_set"]),
            "source_type": record["source_type"],
            "apd_vector": record["apd_vector"],
            "family_flags": record["family_flags"],
            "automorphism_orders": aut_orders,
        }
        records.append(enriched)
        system_tuple_counts[
            (
                aut_orders["lines_plus_mask"],
                aut_orders["source"],
                aut_orders["terminal"],
                aut_orders["combined"],
            )
        ] += 1
        by_terminal_class[enriched["terminal_set_class"]].append(enriched)

    terminal_class_summaries = {}
    for name, group in sorted(by_terminal_class.items()):
        terminal_class_summaries[name] = {
            "pair_count": len(group),
            "mask_counts": counter_json(Counter(row["mask"] for row in group)),
            "source_diagonal_size_counts": counter_json(
                Counter(row["source_diagonal_size"] for row in group)
            ),
            "automorphism_tuple_counts": counter_json(
                Counter(
                    (
                        row["automorphism_orders"]["lines_plus_mask"],
                        row["automorphism_orders"]["source"],
                        row["automorphism_orders"]["terminal"],
                        row["automorphism_orders"]["combined"],
                    )
                    for row in group
                )
            ),
            "complement_fixed_count": sum(
                1 for row in group if row["family_flags"]["complement_fixed"]
            ),
        }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase H extra-32 automorphism/source audit",
            "description": "Colored set-system automorphism orders and terminal-set/source-size split for the 32 structured extras in the main inside-out signature.",
            "automorphism_tuple_order": "lines_plus_mask, source, terminal, combined",
        },
        "extra_pair_count": len(records),
        "automorphism_tuple_counts": counter_json(system_tuple_counts),
        "terminal_set_class_summaries": terminal_class_summaries,
        "records": records,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Extra-32 Set-System Automorphism Audit",
        "",
        "Status: Phase H focused audit of the 32 structured extras",
        "",
        "## Summary",
        "",
        f"- extra pairs: `{result['extra_pair_count']}`",
        "- automorphism tuple order: `lines_plus_mask, source, terminal, combined`",
        f"- automorphism tuple counts: `{result['automorphism_tuple_counts']}`",
        "",
        "## Terminal-Set Classes",
        "",
    ]
    for name, summary in result["terminal_set_class_summaries"].items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"`{summary}`")
        lines.append("")
    lines.extend(
        [
            "## Interpretation",
            "",
            "This audit tests whether the 32 structured extras are separated by a",
            "small colored set-system automorphism signature.  The result should be",
            "read together with the terminal-set and source-diagonal-size split.",
            "",
            "## Guardrail",
            "",
            "This is still a finite fingerprint audit.  It does not prove that the",
            "extras form a natural family outside the tested invariants.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_extra32_automorphism_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "extra32_set_system_automorphisms.json"
        report_path = root / "results" / "EXTRA32_SET_SYSTEM_AUTOMORPHISM_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "extra_pair_count": result["extra_pair_count"],
            "automorphism_tuple_counts": result["automorphism_tuple_counts"],
            "terminal_set_class_summaries": result["terminal_set_class_summaries"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
