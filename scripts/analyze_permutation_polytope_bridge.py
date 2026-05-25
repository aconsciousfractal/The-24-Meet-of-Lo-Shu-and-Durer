"""Permutation-polytope bridge for the D4 -> V4 diagonal break.

Phase D showed that the Durer source diagonals and terminal diagonals are
subgroup/coset tilers in S4, not Type-A poset cones.  The arXiv literature on
permutation polytopes and the Birkhoff graph gives this bridge a cleaner home:

    P(H) = conv{P_sigma : sigma in H}.

This script records exact finite facts for H=D4 and H=V4:

- affine dimensions of P(D4) and P(V4);
- induced Birkhoff-graph edges;
- coset-level dimensions and edge counts.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import magic24_certificates as magic24


Perm = tuple[int, int, int, int]


def perm_from_string(text: str) -> Perm:
    return tuple(int(c) for c in text)  # type: ignore[return-value]


def perm_string(p: Perm) -> str:
    return "".join(str(x) for x in p)


def permutation_matrix_flat(p: Perm) -> list[int]:
    return [1 if p[i] == j else 0 for i in range(4) for j in range(4)]


def rational_rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(x) for x in row] for row in rows if any(row)]
    if not matrix:
        return 0
    r = 0
    c = 0
    cols = len(matrix[0])
    while r < len(matrix) and c < cols:
        pivot = next((i for i in range(r, len(matrix)) if matrix[i][c]), None)
        if pivot is None:
            c += 1
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        pivot_value = matrix[r][c]
        matrix[r] = [x / pivot_value for x in matrix[r]]
        for i in range(len(matrix)):
            if i == r or not matrix[i][c]:
                continue
            factor = matrix[i][c]
            matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[r])]
        r += 1
        c += 1
    return r


def permutation_polytope_dimension(perms: list[Perm]) -> int:
    base = permutation_matrix_flat(perms[0])
    differences = [
        [x - y for x, y in zip(permutation_matrix_flat(p), base)]
        for p in perms[1:]
    ]
    return rational_rank(differences)


def inverse(p: Perm) -> Perm:
    out = [0] * 4
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)  # type: ignore[return-value]


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[q[i]] for i in range(4))  # type: ignore[return-value]


def nontrivial_cycle_lengths(p: Perm) -> list[int]:
    seen = [False] * 4
    lengths = []
    for start in range(4):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            length += 1
            current = p[current]
        if length > 1:
            lengths.append(length)
    return sorted(lengths)


def is_single_cycle(p: Perm) -> bool:
    return len(nontrivial_cycle_lengths(p)) == 1


def birkhoff_edges(perms: list[Perm]) -> list[list[str]]:
    edges = []
    for i, a in enumerate(perms):
        for b in perms[i + 1:]:
            relative = compose(inverse(a), b)
            if is_single_cycle(relative):
                edges.append([perm_string(a), perm_string(b)])
    return edges


def left_cosets(subgroup: list[Perm]) -> list[list[Perm]]:
    all_perms = set(itertools.permutations(range(4)))  # type: ignore[arg-type]
    remaining: set[Perm] = set(all_perms)
    subgroup_set = set(subgroup)
    cosets = []
    while remaining:
        g = min(remaining)
        coset = sorted(compose(g, h) for h in subgroup_set)
        cosets.append(coset)
        remaining -= set(coset)
    return cosets


def subset_record(name: str, perms: list[Perm]) -> dict:
    edges = birkhoff_edges(perms)
    return {
        "name": name,
        "words": [perm_string(p) for p in sorted(perms)],
        "size": len(perms),
        "permutation_polytope_dimension": permutation_polytope_dimension(sorted(perms)),
        "birkhoff_induced_edge_count": len(edges),
        "birkhoff_induced_edges": edges,
        "is_birkhoff_independent_set": len(edges) == 0,
    }


def coset_records(name: str, subgroup: list[Perm]) -> list[dict]:
    out = []
    for index, coset in enumerate(left_cosets(subgroup)):
        record = subset_record(f"{name}_coset_{index}", coset)
        record["index"] = index
        out.append(record)
    return out


def build_permutation_polytope_bridge() -> dict:
    diagonals = magic24.durer_permutation_diagonals()["target_diagonals_by_t"]
    d4 = [perm_from_string(word) for word in diagonals["0"]]
    v4 = [perm_from_string(word) for word in diagonals["1"]]
    d4_record = subset_record("D4_source_diagonals", d4)
    v4_record = subset_record("V4_terminal_diagonals", v4)
    d4_cosets = coset_records("D4", d4)
    v4_cosets = coset_records("V4", v4)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase G",
            "description": "Permutation-polytope and Birkhoff-graph bridge for D4 -> V4.",
            "birkhoff_adjacency": "Two permutations are adjacent iff their relative permutation is one nontrivial cycle.",
        },
        "subsets": {
            "D4": d4_record,
            "V4": v4_record,
        },
        "cosets": {
            "D4": d4_cosets,
            "V4": v4_cosets,
        },
        "comparison": {
            "dimension_drop": f"{d4_record['permutation_polytope_dimension']} -> {v4_record['permutation_polytope_dimension']}",
            "birkhoff_edge_drop": f"{d4_record['birkhoff_induced_edge_count']} -> {v4_record['birkhoff_induced_edge_count']}",
            "all_v4_cosets_are_birkhoff_independent": all(
                row["is_birkhoff_independent_set"] for row in v4_cosets
            ),
            "all_d4_cosets_have_same_dimension_and_edge_count": len(
                {
                    (row["permutation_polytope_dimension"], row["birkhoff_induced_edge_count"])
                    for row in d4_cosets
                }
            )
            == 1,
        },
    }


def write_report(result: dict, path: Path) -> None:
    d4 = result["subsets"]["D4"]
    v4 = result["subsets"]["V4"]
    comparison = result["comparison"]
    lines = [
        "# Permutation-Polytope Bridge Report",
        "",
        "Status: Phase G initial exact replay",
        "",
        "## Core Facts",
        "",
        f"- `dim P(D4)`: `{d4['permutation_polytope_dimension']}`",
        f"- `dim P(V4)`: `{v4['permutation_polytope_dimension']}`",
        f"- Birkhoff induced edges on `D4`: `{d4['birkhoff_induced_edge_count']}`",
        f"- Birkhoff induced edges on `V4`: `{v4['birkhoff_induced_edge_count']}`",
        f"- `V4` is Birkhoff-independent: `{v4['is_birkhoff_independent_set']}`",
        f"- all `V4` cosets are Birkhoff-independent: `{comparison['all_v4_cosets_are_birkhoff_independent']}`",
        "",
        "## Reading",
        "",
        "This is the natural continuation of the Phase-D guardrail.  `D4` and",
        "`V4` are not Type-A poset cones; they are subgroup/coset objects inside",
        "`S4`, and their convex hulls are small permutation polytopes inside the",
        "Birkhoff setting.",
        "",
        "The terminal break has a finite polytope/graph signature:",
        "",
        "```text",
        f"dimension: {comparison['dimension_drop']}",
        f"Birkhoff induced edges: {comparison['birkhoff_edge_drop']}",
        "```",
        "",
        "## Guardrail",
        "",
        "These are exact finite fingerprints.  They do not yet prove that",
        "`P(V4)` is a face of `P(D4)` or of the Birkhoff polytope; that is a",
        "separate face-test branch.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write permutation-polytope bridge JSON and report")
    args = parser.parse_args()

    result = build_permutation_polytope_bridge()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "permutation_polytope_bridge.json"
        report_path = root / "results" / "PERMUTATION_POLYTOPE_BRIDGE_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        print(json.dumps(result["comparison"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
