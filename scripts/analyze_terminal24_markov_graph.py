"""First Markov-style graph audit for terminal-24 endpoint squares.

This is deliberately conservative: it is not a full Markov-basis computation.
The move set consists of primitive fixed-sum diagonal-magic kernel moves with
cell entries in {-1,0,1}.  Nodes are the 236 terminal endpoint squares
`Q - tM` from the Phase-C terminal-24 records.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import sympy as sp

import enumerate_order4_endpoints as order4


Vector = tuple[int, ...]

MAIN_TERMINAL_PROFILE = {
    "edge_count": 107,
    "left_dependencies_Q": 91,
    "rank_F2": 14,
    "rank_Q": 16,
    "right_kernel_Q": 0,
    "snf_counts": {"1": 14, "2": 1, "20": 1},
}
MAIN_TERMINAL_KEY = json.dumps(MAIN_TERMINAL_PROFILE, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def fixed_sum_line_matrix() -> list[list[int]]:
    rows = []
    for i in range(4):
        row = [0] * 16
        for j in range(4):
            row[4 * i + j] = 1
        rows.append(row)
    for j in range(4):
        row = [0] * 16
        for i in range(4):
            row[4 * i + j] = 1
        rows.append(row)
    main = [0] * 16
    anti = [0] * 16
    for i in range(4):
        main[4 * i + i] = 1
        anti[4 * i + (3 - i)] = 1
    rows.extend([main, anti])
    return rows


@lru_cache(maxsize=1)
def integer_kernel_basis() -> tuple[Vector, ...]:
    basis = []
    for vector in sp.Matrix(fixed_sum_line_matrix()).nullspace():
        den = sp.ilcm(*[term.q for term in vector])
        basis.append(tuple(int(term * den) for term in vector))
    return tuple(basis)


def canonical_sign(vector: Vector) -> Vector:
    neg = tuple(-x for x in vector)
    return min(vector, neg)


@lru_cache(maxsize=1)
def primitive_pm1_kernel_moves() -> tuple[Vector, ...]:
    """Primitive fixed-sum magic moves with entries in {-1,0,1}, up to sign."""

    basis = integer_kernel_basis()
    moves: set[Vector] = set()
    for coeffs in itertools.product(range(-2, 3), repeat=len(basis)):
        if all(coeff == 0 for coeff in coeffs):
            continue
        vector = tuple(
            sum(coeff * basis_row[index] for coeff, basis_row in zip(coeffs, basis))
            for index in range(16)
        )
        if not any(vector) or max(abs(entry) for entry in vector) > 1:
            continue
        gcd = 0
        for entry in vector:
            gcd = math.gcd(gcd, abs(entry))
        if gcd == 1:
            moves.add(canonical_sign(vector))
    return tuple(sorted(moves))


def terminal_flat(square: tuple[tuple[int, ...], ...], mask_text: str, t: int) -> Vector:
    mask = tuple(int(char) for char in mask_text)
    return tuple(
        square[i][j] - (t if mask[i] == j else 0)
        for i in range(4)
        for j in range(4)
    )


def node_class(inside_record: dict) -> str:
    if inside_record["is_exact_canonical_v4"]:
        return "exact_v4"
    if inside_record["terminal_signature_key"] == MAIN_TERMINAL_KEY:
        return "main_extra"
    return "outside_main"


def component_profiles(components: list[list[int]], classes: list[str]) -> dict[str, int]:
    profiles = Counter()
    for comp in components:
        counts = Counter(classes[index] for index in comp)
        key = ",".join(f"{name}:{counts[name]}" for name in sorted(counts))
        profiles[key] += 1
    return counter_json(profiles)


def connected_components(adjacency: list[set[int]]) -> list[list[int]]:
    seen: set[int] = set()
    components = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        comp = []
        while stack:
            node = stack.pop()
            comp.append(node)
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components.append(sorted(comp))
    return sorted(components, key=lambda comp: (-len(comp), comp[0]))


@lru_cache(maxsize=1)
def build_terminal24_markov_graph() -> dict:
    root = Path(__file__).resolve().parents[1]
    terminal24 = load_json(root / "results" / "order4_terminal24_fingerprints.json")
    inside_out = load_json(root / "results" / "order4_inside_out_profiles.json")
    inside_by_pair = {
        (record["square_index"], record["mask"]): record
        for record in inside_out["records"]  # type: ignore[index]
    }
    squares = order4.essential_order4_representatives()

    nodes = []
    for record in terminal24["records"]:  # type: ignore[index]
        key = (record["square_index"], record["mask"])
        inside_record = inside_by_pair[key]
        flat = terminal_flat(squares[record["square_index"]], record["mask"], record["t_max"])
        nodes.append(
            {
                "square_index": record["square_index"],
                "mask": record["mask"],
                "terminal_flat": flat,
                "class": node_class(inside_record),
                "terminal_quaterne_count": record["quaternes"]["terminal_count"],
                "terminal_diagonal_is_subgroup": record["terminal_diagonal_is_subgroup"],
                "terminal_diagonal_order_profile": record["terminal_diagonal_order_profile"],
            }
        )

    move_reps = primitive_pm1_kernel_moves()
    signed_moves = set(move_reps) | {tuple(-entry for entry in move) for move in move_reps}
    index_by_flat = {node["terminal_flat"]: idx for idx, node in enumerate(nodes)}
    adjacency = [set() for _ in nodes]
    edge_class_counts: Counter = Counter()
    move_support_counts: Counter = Counter()

    for idx, node in enumerate(nodes):
        flat = node["terminal_flat"]
        for move in signed_moves:
            neighbor_flat = tuple(flat[pos] + move[pos] for pos in range(16))
            neighbor = index_by_flat.get(neighbor_flat)
            if neighbor is None or idx >= neighbor:
                continue
            adjacency[idx].add(neighbor)
            adjacency[neighbor].add(idx)
            edge_class_counts[tuple(sorted((node["class"], nodes[neighbor]["class"])))] += 1
            move_support_counts[sum(1 for entry in move if entry)] += 1

    components = connected_components(adjacency)
    classes = [node["class"] for node in nodes]
    degree_counts = Counter(len(neighbors) for neighbors in adjacency)
    class_degree_counts: dict[str, Counter] = defaultdict(Counter)
    for idx, node in enumerate(nodes):
        class_degree_counts[node["class"]][len(adjacency[idx])] += 1

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase H first terminal-24 Markov-style graph",
            "description": "Graph on terminal endpoint squares using primitive {-1,0,1} fixed-sum diagonal-magic kernel moves.",
            "guardrail": "This is a small-move graph, not a complete Markov-basis theorem.",
        },
        "node_count": len(nodes),
        "move_count_up_to_sign": len(move_reps),
        "signed_move_count": len(signed_moves),
        "move_support_distribution_up_to_sign": counter_json(
            Counter(sum(1 for entry in move if entry) for move in move_reps)
        ),
        "edge_count": sum(len(neighbors) for neighbors in adjacency) // 2,
        "edge_class_counts": counter_json(edge_class_counts),
        "degree_distribution": counter_json(degree_counts),
        "class_degree_distributions": {
            class_name: counter_json(counter)
            for class_name, counter in sorted(class_degree_counts.items())
        },
        "component_count": len(components),
        "component_size_distribution": counter_json(Counter(len(comp) for comp in components)),
        "component_class_profiles": component_profiles(components, classes),
        "largest_components": [
            {
                "size": len(comp),
                "class_counts": counter_json(Counter(classes[index] for index in comp)),
                "node_indices": comp,
            }
            for comp in components[:12]
        ],
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Terminal-24 Markov-Style Graph",
        "",
        "Status: Phase H first small-move connectivity audit",
        "",
        "## Scope",
        "",
        "Nodes are the `236` terminal endpoint squares `Q-tM` from the Phase-C",
        "terminal-24 records.  Edges use primitive fixed-sum diagonal-magic",
        "kernel moves with entries in `{-1,0,1}`.",
        "",
        "This is not a full Markov-basis theorem.",
        "",
        "## Summary",
        "",
        f"- nodes: `{result['node_count']}`",
        f"- primitive moves up to sign: `{result['move_count_up_to_sign']}`",
        f"- signed moves: `{result['signed_move_count']}`",
        f"- move support distribution up to sign: `{result['move_support_distribution_up_to_sign']}`",
        f"- edges: `{result['edge_count']}`",
        f"- degree distribution: `{result['degree_distribution']}`",
        f"- components: `{result['component_count']}`",
        f"- component size distribution: `{result['component_size_distribution']}`",
        "",
        "## Class Interaction",
        "",
        f"- edge class counts: `{result['edge_class_counts']}`",
        f"- class degree distributions: `{result['class_degree_distributions']}`",
        f"- component class profiles: `{result['component_class_profiles']}`",
        "",
        "## Interpretation",
        "",
        "The small-move graph is highly disconnected.  It mostly connects exact",
        "`V4` records to other exact `V4` records, while many outside-main and",
        "main-extra records are isolated or only lightly attached.",
        "",
        "## Guardrail",
        "",
        "Do not claim endpoint-24 Markov connectivity from this graph.  The",
        "computed graph is a conservative first audit using only primitive",
        "`{-1,0,1}` kernel moves.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_terminal24_markov_graph()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "terminal24_markov_graph.json"
        report_path = root / "results" / "TERMINAL24_MARKOV_GRAPH_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "node_count": result["node_count"],
            "move_count_up_to_sign": result["move_count_up_to_sign"],
            "edge_count": result["edge_count"],
            "component_count": result["component_count"],
            "component_size_distribution": result["component_size_distribution"],
            "edge_class_counts": result["edge_class_counts"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
