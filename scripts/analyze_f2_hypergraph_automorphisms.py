"""Automorphism audit for the Phase-F Durer/Sagrada hypergraphs.

The vertices are the Durer value-minus-one labels 0..15.  Hyperedges are
four-label subsets.  We compute automorphisms by converting each hypergraph
to a colored incidence graph and enumerating graph automorphisms with
NetworkX's VF2 matcher.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Iterable

import networkx as nx


LabelSet = tuple[int, int, int, int]
Perm = tuple[int, ...]

SAGRADA_LABEL_SET = frozenset((10, 11, 14, 15))


def label_word(labels: Iterable[int]) -> str:
    return "".join("0123456789ABCDEF"[label] for label in labels)


def source_sum(labels: Iterable[int]) -> int:
    return sum(label + 1 for label in labels)


def mask_incidence(labels: Iterable[int]) -> int:
    return len(set(labels) & SAGRADA_LABEL_SET)


def terminal_sum(labels: Iterable[int], t: int = 10) -> int:
    return source_sum(labels) - t * mask_incidence(labels)


def is_affine_plane(labels: Iterable[int]) -> bool:
    out = 0
    labels_tuple = tuple(labels)
    for label in labels_tuple:
        out ^= label
    return len(labels_tuple) == 4 and len(set(labels_tuple)) == 4 and out == 0


def all_label_quads() -> list[LabelSet]:
    return list(itertools.combinations(range(16), 4))  # type: ignore[return-value]


def h34_edges() -> list[LabelSet]:
    return [quad for quad in all_label_quads() if source_sum(quad) == 34]


def h24_edges() -> list[LabelSet]:
    return [quad for quad in all_label_quads() if terminal_sum(quad) == 24]


def h24_source_color(edge: LabelSet) -> str:
    return f"source_{source_sum(edge)}_incidence_{mask_incidence(edge)}"


def affine_color(edge: LabelSet) -> str:
    return "affine" if is_affine_plane(edge) else "non_affine"


def h24_source_affine_color(edge: LabelSet) -> str:
    return f"{h24_source_color(edge)}_{affine_color(edge)}"


def build_incidence_graph(
    edges: list[LabelSet], edge_color: Callable[[LabelSet], str]
) -> nx.Graph:
    graph = nx.Graph()
    for label in range(16):
        graph.add_node(("v", label), kind="vertex", color="cell")
    for idx, edge in enumerate(edges):
        edge_node = ("e", idx)
        graph.add_node(edge_node, kind="edge", color=edge_color(edge), edge=edge)
        for label in edge:
            graph.add_edge(("v", label), edge_node)
    return graph


def enumerate_cell_automorphisms(
    edges: list[LabelSet], edge_color: Callable[[LabelSet], str]
) -> list[Perm]:
    graph = build_incidence_graph(edges, edge_color)

    def node_match(left: dict, right: dict) -> bool:
        return left["kind"] == right["kind"] and left["color"] == right["color"]

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph, graph, node_match=node_match
    )
    perms = {
        tuple(morphism[("v", label)][1] for label in range(16))
        for morphism in matcher.isomorphisms_iter()
    }
    return sorted(perms)


def cycle_type(perm: Perm) -> tuple[int, ...]:
    seen = [False] * len(perm)
    lengths = []
    for start in range(len(perm)):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            length += 1
            current = perm[current]
        lengths.append(length)
    return tuple(sorted(lengths))


def cycle_type_string(cycle_type_tuple: tuple[int, ...]) -> str:
    counts = Counter(cycle_type_tuple)
    return " ".join(f"{length}^{counts[length]}" for length in sorted(counts))


def group_orbits(perms: list[Perm], elements: Iterable[int]) -> list[tuple[int, ...]]:
    elements_tuple = tuple(elements)
    parent = {element: element for element in elements_tuple}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b:
            parent[root_b] = root_a

    for perm in perms:
        for element in elements_tuple:
            union(element, perm[element])

    buckets: dict[int, list[int]] = defaultdict(list)
    for element in elements_tuple:
        buckets[find(element)].append(element)
    return sorted(
        (tuple(sorted(bucket)) for bucket in buckets.values()),
        key=lambda item: (len(item), item),
    )


def set_orbits(perms: list[Perm], sets: Iterable[Iterable[int]]) -> list[tuple[LabelSet, ...]]:
    universe = {tuple(sorted(edge)) for edge in sets}
    remaining = set(universe)
    orbits = []
    while remaining:
        seed = remaining.pop()
        orbit = {
            tuple(sorted(perm[label] for label in seed))
            for perm in perms
        }
        orbit &= universe
        remaining -= orbit
        orbits.append(tuple(sorted(orbit)))
    return sorted(orbits, key=lambda item: (len(item), item[0]))


def edge_color_distribution(
    edges: list[LabelSet], edge_color: Callable[[LabelSet], str]
) -> dict[str, int]:
    return dict(sorted(Counter(edge_color(edge) for edge in edges).items()))


def automorphism_case(
    name: str,
    edges: list[LabelSet],
    edge_color: Callable[[LabelSet], str],
) -> dict:
    perms = enumerate_cell_automorphisms(edges, edge_color)
    vertex_orbits = group_orbits(perms, range(16))
    edge_orbits = set_orbits(perms, edges)
    sagrada_orbit = {
        tuple(sorted(perm[label] for label in SAGRADA_LABEL_SET))
        for perm in perms
    }
    cycle_profile = Counter(cycle_type_string(cycle_type(perm)) for perm in perms)

    return {
        "name": name,
        "edge_count": len(edges),
        "edge_color_distribution": edge_color_distribution(edges, edge_color),
        "automorphism_group_order": len(perms),
        "cell_orbits": [list(orbit) for orbit in vertex_orbits],
        "cell_orbit_size_distribution": dict(sorted(Counter(len(orbit) for orbit in vertex_orbits).items())),
        "edge_orbit_size_distribution": dict(sorted(Counter(len(orbit) for orbit in edge_orbits).items())),
        "sagrada_mask_orbit_count": len(sagrada_orbit),
        "sagrada_mask_stabilizer_order": sum(
            1
            for perm in perms
            if {perm[label] for label in SAGRADA_LABEL_SET} == set(SAGRADA_LABEL_SET)
        ),
        "cycle_type_profile": dict(sorted(cycle_profile.items())),
        "sample_permutations": [label_word(perm) for perm in perms[:12]],
    }


def build_hypergraph_automorphism_audit() -> dict:
    source_h34 = h34_edges()
    terminal_h24 = h24_edges()
    cases = [
        automorphism_case("H34_all", source_h34, lambda edge: "edge"),
        automorphism_case("H34_affine_colored", source_h34, affine_color),
        automorphism_case(
            "H34_affine_only",
            [edge for edge in source_h34 if is_affine_plane(edge)],
            lambda edge: "affine",
        ),
        automorphism_case("H24_all", terminal_h24, lambda edge: "edge"),
        automorphism_case("H24_affine_colored", terminal_h24, affine_color),
        automorphism_case("H24_source_colored", terminal_h24, h24_source_color),
        automorphism_case(
            "H24_source_affine_colored", terminal_h24, h24_source_affine_color
        ),
    ]

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase F automorphism audit",
            "description": "Colored hypergraph automorphism groups for H34(D) and H24(D(10)) in the Durer value-label model.",
            "method": "Colored incidence graph automorphisms via networkx VF2.",
        },
        "sagrada_label_set": sorted(SAGRADA_LABEL_SET),
        "cases": cases,
        "case_by_name": {case["name"]: case for case in cases},
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# F2 Hypergraph Automorphism Report",
        "",
        "Status: Phase F colored automorphism audit",
        "",
        "## Method",
        "",
        "Each hypergraph is encoded as a colored incidence graph with 16 cell",
        "vertices and one edge-node per quaterne.  Automorphisms are graph",
        "automorphisms preserving node kind and color.",
        "",
        "## Results",
        "",
    ]
    for case in result["cases"]:
        lines.extend(
            [
                f"### {case['name']}",
                "",
                f"- edges: `{case['edge_count']}`",
                f"- edge colors: `{case['edge_color_distribution']}`",
                f"- automorphism group order: `{case['automorphism_group_order']}`",
                f"- cell orbit sizes: `{case['cell_orbit_size_distribution']}`",
                f"- edge orbit sizes: `{case['edge_orbit_size_distribution']}`",
                f"- Sagrada mask orbit count: `{case['sagrada_mask_orbit_count']}`",
                f"- Sagrada mask stabilizer order: `{case['sagrada_mask_stabilizer_order']}`",
                f"- cycle type profile: `{case['cycle_type_profile']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation",
            "",
            "- `H34_all` has only the identity and value-complement symmetry.",
            "- The affine sublayer `H34_affine_only` is much more symmetric, with",
            "  group order `384` and transitive action on the 16 labels.",
            "- `H24_all` has a 16-element automorphism group, but affine coloring",
            "  collapses it to order `2`.",
            "- Coloring `H24` by source sum and mask incidence collapses the group",
            "  to the identity.",
            "",
            "## Guardrail",
            "",
            "The terminal hypergraph has nontrivial uncolored symmetries, but the",
            "transport decomposition `25+50+21` is rigid in the fixed value-label",
            "model.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_hypergraph_automorphism_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "f2_hypergraph_automorphisms.json"
        report_path = root / "results" / "F2_HYPERGRAPH_AUTOMORPHISM_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            case["name"]: {
                "edges": case["edge_count"],
                "automorphism_group_order": case["automorphism_group_order"],
                "sagrada_mask_stabilizer_order": case["sagrada_mask_stabilizer_order"],
            }
            for case in result["cases"]
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
