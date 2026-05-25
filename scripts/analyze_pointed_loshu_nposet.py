"""Pointed Lo Shu S=24 vs N-poset five-state bridge.

This is a small Phase-G guardrail certificate.  It verifies that the bare
cardinality match 5=5 is weak, while a pointed Lo Shu boundary graph is
isomorphic to both the linear-extension graph of the N-poset and the Hasse
graph of the order-ideal lattice J(A2+).
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

import networkx as nx


LO_SHU_POINTS = {
    "O": (0, 0),
    "E": (1, 0),
    "N": (0, 1),
    "W": (-1, 0),
    "S": (0, -1),
}

BOUNDARY_CYCLE = ("E", "N", "W", "S")
N_POSET_RELATIONS = (("a", "b"), ("c", "b"), ("c", "d"))
A2_RELATIONS = (("alpha", "alpha+beta"), ("beta", "alpha+beta"))


def lo_shu_square(a: int, b: int, g: int = 8) -> list[list[int]]:
    return [
        [g + a, g - a - b, g + b],
        [g - a + b, g, g + a - b],
        [g - b, g + a + b, g - a],
    ]


def graph_from_edges(vertices: Iterable[str], edges: Iterable[tuple[str, str]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(tuple(sorted(edge)) for edge in edges)
    return graph


def sorted_edges(graph: nx.Graph) -> list[list[str]]:
    return [list(edge) for edge in sorted(tuple(sorted(edge)) for edge in graph.edges())]


def degree_sequence(graph: nx.Graph) -> list[int]:
    return sorted([degree for _, degree in graph.degree()])


def automorphism_order(graph: nx.Graph) -> int:
    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
    return sum(1 for _ in matcher.isomorphisms_iter())


def natural_loshu_graph() -> nx.Graph:
    return graph_from_edges(
        LO_SHU_POINTS,
        (("O", boundary) for boundary in BOUNDARY_CYCLE),
    )


def pointed_loshu_graph(mark: str = "E") -> nx.Graph:
    cycle_edges = list(zip(BOUNDARY_CYCLE, BOUNDARY_CYCLE[1:] + BOUNDARY_CYCLE[:1]))
    return graph_from_edges(LO_SHU_POINTS, cycle_edges + [(mark, "O")])


def transitive_closure(relations: Iterable[tuple[str, str]]) -> set[tuple[str, str]]:
    closure = set(relations)
    changed = True
    while changed:
        changed = False
        additions = {
            (a, d)
            for a, b in closure
            for c, d in closure
            if b == c and (a, d) not in closure
        }
        if additions:
            closure |= additions
            changed = True
    return closure


def is_linear_extension(word: tuple[str, ...], relations: Iterable[tuple[str, str]]) -> bool:
    position = {letter: idx for idx, letter in enumerate(word)}
    return all(position[left] < position[right] for left, right in relations)


def n_poset_linear_extensions() -> list[str]:
    letters = tuple("abcd")
    return [
        "".join(word)
        for word in itertools.permutations(letters)
        if is_linear_extension(word, N_POSET_RELATIONS)
    ]


def n_poset_linear_extension_graph() -> nx.Graph:
    extensions = n_poset_linear_extensions()
    extension_set = set(extensions)
    closure = transitive_closure(N_POSET_RELATIONS)
    edges = set()
    for word in extensions:
        letters = list(word)
        for idx in range(len(letters) - 1):
            left = letters[idx]
            right = letters[idx + 1]
            if (left, right) in closure or (right, left) in closure:
                continue
            swapped = letters[:]
            swapped[idx], swapped[idx + 1] = swapped[idx + 1], swapped[idx]
            swapped_word = "".join(swapped)
            if swapped_word in extension_set:
                edges.add(tuple(sorted((word, swapped_word))))
    return graph_from_edges(extensions, edges)


def order_ideals(elements: Iterable[str], relations: Iterable[tuple[str, str]]) -> list[tuple[str, ...]]:
    elements_tuple = tuple(elements)
    closure = transitive_closure(relations)
    ideals = []
    for mask in range(1 << len(elements_tuple)):
        subset = {
            element
            for idx, element in enumerate(elements_tuple)
            if (mask >> idx) & 1
        }
        downward_closed = all(
            lower in subset
            for lower, upper in closure
            if upper in subset
        )
        if downward_closed:
            ideals.append(tuple(sorted(subset, key=elements_tuple.index)))
    return sorted(ideals, key=lambda item: (len(item), item))


def ideal_label(ideal: Iterable[str]) -> str:
    values = tuple(ideal)
    return "{}" if not values else "{" + ",".join(values) + "}"


def a2_order_ideal_graph() -> nx.Graph:
    elements = ("alpha", "beta", "alpha+beta")
    ideals = order_ideals(elements, A2_RELATIONS)
    labels = [ideal_label(ideal) for ideal in ideals]
    edges = []
    for left, right in itertools.combinations(ideals, 2):
        if abs(len(left) - len(right)) != 1:
            continue
        if set(left) < set(right) or set(right) < set(left):
            edges.append((ideal_label(left), ideal_label(right)))
    return graph_from_edges(labels, edges)


def verify_mapping(
    source_graph: nx.Graph,
    target_graph: nx.Graph,
    mapping: dict[str, str],
) -> bool:
    source_edges = {tuple(sorted(edge)) for edge in source_graph.edges()}
    mapped_edges = {
        tuple(sorted((mapping[left], mapping[right])))
        for left, right in source_edges
    }
    target_edges = {tuple(sorted(edge)) for edge in target_graph.edges()}
    return mapped_edges == target_edges and set(mapping.values()) == set(target_graph.nodes())


def graph_record(graph: nx.Graph) -> dict:
    return {
        "vertex_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "vertices": sorted(graph.nodes()),
        "edges": sorted_edges(graph),
        "degree_sequence": degree_sequence(graph),
        "automorphism_order": automorphism_order(graph),
    }


def build_pointed_loshu_nposet_analysis() -> dict:
    natural = natural_loshu_graph()
    pointed = pointed_loshu_graph("E")
    n_graph = n_poset_linear_extension_graph()
    a2_graph = a2_order_ideal_graph()

    loshu_to_n = {
        "E": "cadb",
        "O": "cdab",
        "N": "acdb",
        "W": "acbd",
        "S": "cabd",
    }
    loshu_to_a2 = {
        "E": "{alpha,beta}",
        "O": "{alpha,beta,alpha+beta}",
        "N": "{alpha}",
        "W": "{}",
        "S": "{beta}",
    }

    pointed_by_mark = {
        mark: {
            "graph": graph_record(pointed_loshu_graph(mark)),
            "isomorphic_to_n_poset_graph": nx.is_isomorphic(
                pointed_loshu_graph(mark), n_graph
            ),
        }
        for mark in BOUNDARY_CYCLE
    }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase G pointed five-state bridge",
            "description": "Tests the pointed Lo Shu S=24 fiber against the N-poset linear-extension graph and J(A2+) order-ideal graph.",
        },
        "lo_shu_s24_points": {
            name: {
                "coordinates": list(coords),
                "square": lo_shu_square(*coords),
            }
            for name, coords in LO_SHU_POINTS.items()
        },
        "natural_loshu_graph": graph_record(natural),
        "pointed_loshu_graph_mark_E": graph_record(pointed),
        "n_poset": {
            "relations": [list(relation) for relation in N_POSET_RELATIONS],
            "linear_extensions": n_poset_linear_extensions(),
            "linear_extension_graph": graph_record(n_graph),
        },
        "a2_positive_root_poset": {
            "relations": [list(relation) for relation in A2_RELATIONS],
            "order_ideals": sorted(a2_graph.nodes(), key=lambda item: (len(item), item)),
            "order_ideal_graph": graph_record(a2_graph),
        },
        "comparisons": {
            "natural_loshu_isomorphic_to_n_poset_graph": nx.is_isomorphic(natural, n_graph),
            "pointed_loshu_isomorphic_to_n_poset_graph": nx.is_isomorphic(pointed, n_graph),
            "pointed_loshu_isomorphic_to_a2_ideal_graph": nx.is_isomorphic(pointed, a2_graph),
            "n_poset_graph_isomorphic_to_a2_ideal_graph": nx.is_isomorphic(n_graph, a2_graph),
            "explicit_loshu_to_n_mapping_verified": verify_mapping(pointed, n_graph, loshu_to_n),
            "explicit_loshu_to_a2_mapping_verified": verify_mapping(pointed, a2_graph, loshu_to_a2),
        },
        "explicit_mappings": {
            "pointed_loshu_E_to_n_poset_extensions": loshu_to_n,
            "pointed_loshu_E_to_a2_order_ideals": loshu_to_a2,
        },
        "pointed_boundary_mark_variants": pointed_by_mark,
        "boundary_mark_count": len(BOUNDARY_CYCLE),
        "all_boundary_marks_give_isomorphic_graphs": all(
            row["isomorphic_to_n_poset_graph"] for row in pointed_by_mark.values()
        ),
        "degree_sequence_counts": {
            "natural_loshu": counter_json(Counter(degree_sequence(natural))),
            "pointed_loshu": counter_json(Counter(degree_sequence(pointed))),
            "n_poset": counter_json(Counter(degree_sequence(n_graph))),
            "a2_order_ideals": counter_json(Counter(degree_sequence(a2_graph))),
        },
    }


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter)}


def write_report(result: dict, path: Path) -> None:
    comparisons = result["comparisons"]
    lines = [
        "# Pointed Lo Shu / N-Poset Bridge Report",
        "",
        "Status: Phase G pointed five-state bridge audit",
        "",
        "## Summary",
        "",
        f"- natural Lo Shu graph isomorphic to N-poset graph: `{comparisons['natural_loshu_isomorphic_to_n_poset_graph']}`",
        f"- pointed Lo Shu graph isomorphic to N-poset graph: `{comparisons['pointed_loshu_isomorphic_to_n_poset_graph']}`",
        f"- pointed Lo Shu graph isomorphic to `J(A2+)`: `{comparisons['pointed_loshu_isomorphic_to_a2_ideal_graph']}`",
        f"- N-poset graph isomorphic to `J(A2+)`: `{comparisons['n_poset_graph_isomorphic_to_a2_ideal_graph']}`",
        f"- explicit Lo Shu -> N-poset mapping verified: `{comparisons['explicit_loshu_to_n_mapping_verified']}`",
        f"- explicit Lo Shu -> A2 mapping verified: `{comparisons['explicit_loshu_to_a2_mapping_verified']}`",
        f"- all boundary marks give isomorphic graphs: `{result['all_boundary_marks_give_isomorphic_graphs']}`",
        "",
        "## N-Poset Linear Extensions",
        "",
        "```text",
        *result["n_poset"]["linear_extensions"],
        "```",
        "",
        "## Explicit Pointed Map",
        "",
        "Lo Shu mark `E` is the degree-3 vertex and `O` is the pendant vertex.",
        "",
        "```text",
        *[
            f"{left} -> {right}"
            for left, right in result["explicit_mappings"][
                "pointed_loshu_E_to_n_poset_extensions"
            ].items()
        ],
        "```",
        "",
        "## Interpretation",
        "",
        "The bare cardinality `5=5` is not enough: the natural Lo Shu lattice",
        "adjacency graph is not the N-poset linear-extension graph.  The",
        "isomorphism appears only after adding a boundary cycle and marking one",
        "boundary point to attach the center.",
        "",
        "This is a coherent branch, but it is pointed rather than canonical.  The",
        "open mathematical question is whether the marked boundary point can be",
        "selected non-arbitrarily from Sagrada terminality, `D4 -> V4`, APD/PTE,",
        "or the `F2^4` layer.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_pointed_loshu_nposet_analysis()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "pointed_loshu_nposet_bridge.json"
        report_path = root / "results" / "POINTED_LOSHU_NPOSET_BRIDGE_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        print(json.dumps(result["comparisons"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
