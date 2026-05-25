"""Phase H inside-out / set-system audit for Durer/Sagrada."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Iterable

import networkx as nx
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

import magic24_certificates as magic24


Cell = tuple[int, int]
Edge = tuple[Cell, ...]


def cell_label(cell: Cell) -> str:
    return f"r{cell[0]}c{cell[1]}"


def all_cells() -> list[Cell]:
    return [(i, j) for i in range(4) for j in range(4)]


def normalize_edge(cells: Iterable[Cell]) -> Edge:
    return tuple(sorted(cells))


def row_edge(i: int) -> Edge:
    return normalize_edge((i, j) for j in range(4))


def col_edge(j: int) -> Edge:
    return normalize_edge((i, j) for i in range(4))


def main_diag_edge() -> Edge:
    return normalize_edge((i, i) for i in range(4))


def anti_diag_edge() -> Edge:
    return normalize_edge((i, 3 - i) for i in range(4))


def sagrada_edge() -> Edge:
    return normalize_edge((i, magic24.SAGRADA_MASK_PERM[i]) for i in range(4))


def source_sum(edge: Edge) -> int:
    return sum(magic24.d_value(i, j) for i, j in edge)


def mask_incidence(edge: Edge) -> int:
    return magic24.mask_incidence(edge)


def terminal_sum(edge: Edge, t: int = 10) -> int:
    return source_sum(edge) - t * mask_incidence(edge)


def h34_edges() -> list[Edge]:
    return [
        normalize_edge(edge)
        for edge in itertools.combinations(all_cells(), 4)
        if source_sum(normalize_edge(edge)) == 34
    ]


def h24_edges() -> list[Edge]:
    return [
        normalize_edge(edge)
        for edge in itertools.combinations(all_cells(), 4)
        if terminal_sum(normalize_edge(edge)) == 24
    ]


def base_line_records() -> list[dict]:
    records = []
    for i in range(4):
        records.append({"name": f"row_{i}", "color": "row", "edge": row_edge(i)})
    for j in range(4):
        records.append({"name": f"col_{j}", "color": "col", "edge": col_edge(j)})
    records.append({"name": "diag_main", "color": "diag_main", "edge": main_diag_edge()})
    records.append({"name": "diag_anti", "color": "diag_anti", "edge": anti_diag_edge()})
    return records


def edge_records_for_system(system: str) -> list[dict]:
    records = base_line_records()
    if system in {"lines_plus_mask", "source", "terminal", "combined"}:
        records.append({"name": "sagrada_mask", "color": "mask", "edge": sagrada_edge()})
    if system in {"source", "combined"}:
        for index, edge in enumerate(h34_edges()):
            records.append(
                {
                    "name": f"h34_{index}",
                    "color": f"h34_incidence_{mask_incidence(edge)}",
                    "edge": edge,
                    "source_sum": source_sum(edge),
                    "mask_incidence": mask_incidence(edge),
                }
            )
    if system in {"terminal", "combined"}:
        for index, edge in enumerate(h24_edges()):
            records.append(
                {
                    "name": f"h24_{index}",
                    "color": f"h24_source_{source_sum(edge)}_incidence_{mask_incidence(edge)}",
                    "edge": edge,
                    "source_sum": source_sum(edge),
                    "mask_incidence": mask_incidence(edge),
                    "terminal_sum": terminal_sum(edge),
                }
            )
    return records


def incidence_matrix(records: list[dict]) -> list[list[int]]:
    cell_index = {cell: idx for idx, cell in enumerate(all_cells())}
    rows = []
    for record in records:
        edge = set(record["edge"])
        rows.append([1 if cell in edge else 0 for cell in all_cells()])
    return rows


def rank_over_q(matrix: list[list[int]]) -> int:
    return int(sp.Matrix(matrix).rank())


def rank_over_f2(matrix: list[list[int]]) -> int:
    rows = []
    for row in matrix:
        value = 0
        for bit, entry in enumerate(row):
            if entry % 2:
                value |= 1 << bit
        rows.append(value)
    rank = 0
    for bit in reversed(range(16)):
        pivot = next((idx for idx in range(rank, len(rows)) if rows[idx] & (1 << bit)), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for idx in range(len(rows)):
            if idx != rank and rows[idx] & (1 << bit):
                rows[idx] ^= rows[rank]
        rank += 1
    return rank


def snf_summary(matrix: list[list[int]]) -> dict:
    snf = smith_normal_form(sp.Matrix(matrix))
    diag = []
    for idx in range(min(snf.rows, snf.cols)):
        value = int(abs(snf[idx, idx]))
        if value:
            diag.append(value)
    counts = Counter(diag)
    return {
        "nonzero_diagonal": diag,
        "nonzero_diagonal_counts": {str(k): counts[k] for k in sorted(counts)},
        "nonunit_diagonal": [value for value in diag if value != 1],
    }


def rational_nullspace_basis(matrix: list[list[int]], side: str) -> list[list[str]]:
    mat = sp.Matrix(matrix)
    if side == "right":
        basis = mat.nullspace()
    elif side == "left":
        basis = mat.T.nullspace()
    else:
        raise ValueError(side)
    return [[str(entry) for entry in vector] for vector in basis[:8]]


def build_incidence_graph(records: list[dict]) -> nx.Graph:
    graph = nx.Graph()
    for cell in all_cells():
        graph.add_node(("cell", cell), kind="cell", color="cell")
    for idx, record in enumerate(records):
        node = ("edge", idx)
        graph.add_node(node, kind="edge", color=record["color"])
        for cell in record["edge"]:
            graph.add_edge(("cell", cell), node)
    return graph


def enumerate_cell_automorphisms(records: list[dict]) -> list[tuple[Cell, ...]]:
    graph = build_incidence_graph(records)

    def node_match(left: dict, right: dict) -> bool:
        return left["kind"] == right["kind"] and left["color"] == right["color"]

    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph, node_match=node_match)
    perms = {
        tuple(morphism[("cell", cell)][1] for cell in all_cells())
        for morphism in matcher.isomorphisms_iter()
    }
    return sorted(perms)


def cell_orbits(perms: list[tuple[Cell, ...]]) -> list[list[str]]:
    cells = all_cells()
    parent = {cell: cell for cell in cells}

    def find(cell: Cell) -> Cell:
        while parent[cell] != cell:
            parent[cell] = parent[parent[cell]]
            cell = parent[cell]
        return cell

    def union(left: Cell, right: Cell) -> None:
        root_left = find(left)
        root_right = find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    for perm in perms:
        mapping = dict(zip(cells, perm))
        for cell in cells:
            union(cell, mapping[cell])

    buckets: dict[Cell, list[Cell]] = defaultdict(list)
    for cell in cells:
        buckets[find(cell)].append(cell)
    return [
        [cell_label(cell) for cell in sorted(bucket)]
        for bucket in sorted(buckets.values(), key=lambda item: (len(item), item))
    ]


def automorphism_summary(records: list[dict]) -> dict:
    perms = enumerate_cell_automorphisms(records)
    return {
        "automorphism_group_order": len(perms),
        "cell_orbits": cell_orbits(perms),
        "cell_orbit_size_distribution": dict(sorted(Counter(len(orbit) for orbit in cell_orbits(perms)).items())),
        "sample_permutations": [
            [cell_label(cell) for cell in perm] for perm in perms[:8]
        ],
    }


def system_summary(name: str) -> dict:
    records = edge_records_for_system(name)
    matrix = incidence_matrix(records)
    rank_q = rank_over_q(matrix)
    rank_f2 = rank_over_f2(matrix)
    edge_colors = Counter(record["color"] for record in records)
    return {
        "name": name,
        "edge_count": len(records),
        "edge_color_counts": dict(sorted(edge_colors.items())),
        "rank_over_Q": rank_q,
        "rank_over_F2": rank_f2,
        "right_kernel_dimension_over_Q": 16 - rank_q,
        "left_dependency_dimension_over_Q": len(records) - rank_q,
        "snf": snf_summary(matrix),
        "right_kernel_basis_sample": rational_nullspace_basis(matrix, "right"),
        "left_dependency_basis_sample": rational_nullspace_basis(matrix, "left"),
        "automorphisms": automorphism_summary(records),
    }


def build_inside_out_set_system_audit() -> dict:
    systems = [
        system_summary("magic_lines"),
        system_summary("lines_plus_mask"),
        system_summary("source"),
        system_summary("terminal"),
        system_summary("combined"),
    ]
    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase H inside-out set-system audit",
            "description": "Incidence rank/SNF/kernel/aut audit for Durer/Sagrada row-column-diagonal-mask-quaterne set systems.",
            "cell_order": [cell_label(cell) for cell in all_cells()],
        },
        "h34_count": len(h34_edges()),
        "h24_count": len(h24_edges()),
        "systems": systems,
        "system_by_name": {system["name"]: system for system in systems},
        "interpretation": {
            "rank_goal": "Check whether adding Durer/Sagrada hyperedges cuts the 16-cell label space to full rank.",
            "inside_out_scope": "This is a set-system incidence audit, not yet an Ehrhart or Hilbert-basis computation.",
        },
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Inside-Out Set-System Audit",
        "",
        "Status: Phase H first set-system certificate",
        "",
        "## Counts",
        "",
        f"- `H34(D)` quaternes: `{result['h34_count']}`",
        f"- `H24(D(10))` quaternes: `{result['h24_count']}`",
        "",
        "## Systems",
        "",
    ]
    for system in result["systems"]:
        lines.extend(
            [
                f"### {system['name']}",
                "",
                f"- edge count: `{system['edge_count']}`",
                f"- edge colors: `{system['edge_color_counts']}`",
                f"- rank over Q: `{system['rank_over_Q']}`",
                f"- rank over F2: `{system['rank_over_F2']}`",
                f"- right kernel dimension over Q: `{system['right_kernel_dimension_over_Q']}`",
                f"- left dependency dimension over Q: `{system['left_dependency_dimension_over_Q']}`",
                f"- SNF diagonal counts: `{system['snf']['nonzero_diagonal_counts']}`",
                f"- SNF nonunit diagonal: `{system['snf']['nonunit_diagonal']}`",
                f"- automorphism group order: `{system['automorphisms']['automorphism_group_order']}`",
                f"- cell orbit sizes: `{system['automorphisms']['cell_orbit_size_distribution']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation",
            "",
            "This turns the inside-out/magic-labelling vocabulary into a concrete",
            "finite set-system.  The source, terminal, and combined systems can now",
            "be compared by incidence rank, integral SNF data, kernel dimensions,",
            "and colored automorphism groups.",
            "",
            "## Guardrail",
            "",
            "This is not yet an Ehrhart count, Hilbert-basis decomposition, or",
            "inside-out polytope theorem.  It is the incidence substrate those",
            "later computations can use.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_inside_out_set_system_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "inside_out_set_system_audit.json"
        report_path = root / "results" / "INSIDE_OUT_SET_SYSTEM_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            system["name"]: {
                "edge_count": system["edge_count"],
                "rank_Q": system["rank_over_Q"],
                "rank_F2": system["rank_over_F2"],
                "right_kernel": system["right_kernel_dimension_over_Q"],
                "aut_order": system["automorphisms"]["automorphism_group_order"],
                "snf": system["snf"]["nonzero_diagonal_counts"],
            }
            for system in result["systems"]
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
