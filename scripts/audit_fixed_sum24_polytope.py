"""Audit the full fixed-sum S=24 bounded order-4 magic polytope.

This is the heavier Phase-E audit.  It enumerates vertices of the full
fixed-sum S=24 polytope:

    1 <= x_ij <= 16
    every row/column/main diagonal sums to 24.

The enumeration uses floating point only as a fast filter.  Every accepted
candidate is reconstructed and verified over Q before being recorded.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "analyze_bounded_magic_polytope.py"

spec = importlib.util.spec_from_file_location("bounded_magic_polytope", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)


def flatten_square(matrix: list[list[int | str]]) -> tuple[Fraction, ...]:
    return tuple(Fraction(x) for row in matrix for x in row)


def audit_fixed_sum24_polytope() -> dict[str, Any]:
    n = 4
    magic_sum = 24
    lo = 1
    hi = 16
    variable_count = n * n

    rows = base.fixed_magic_equations(n)
    rhs = base.fixed_magic_rhs(n, magic_sum)
    affine = base.affine_solution_space(rows, rhs, variable_count)
    if affine is None:
        raise ValueError("fixed-sum affine space is empty")
    particular, basis = affine
    dimension = len(basis)

    particular_float = np.array([float(x) for x in particular])
    basis_float = np.array(
        [[float(vector[i]) for vector in basis] for i in range(variable_count)]
    )

    hyperplanes = []
    for idx in range(variable_count):
        coeff_float = np.array([float(vector[idx]) for vector in basis])
        coeff_exact = [vector[idx] for vector in basis]
        for value in (lo, hi):
            rhs_exact = Fraction(value) - particular[idx]
            hyperplanes.append(
                {
                    "index": idx,
                    "value": value,
                    "coeff_float": coeff_float,
                    "rhs_float": float(rhs_exact),
                    "coeff_exact": coeff_exact,
                    "rhs_exact": rhs_exact,
                }
            )

    vertices: dict[tuple[Fraction, ...], dict[str, Any]] = {}
    checked_combinations = 0
    feasible_combinations = 0
    exact_feasible_combinations = 0
    singular_combinations = 0

    for chosen_indices in itertools.combinations(range(len(hyperplanes)), dimension):
        checked_combinations += 1
        chosen = [hyperplanes[i] for i in chosen_indices]
        matrix_float = np.stack([item["coeff_float"] for item in chosen])
        rhs_float = np.array([item["rhs_float"] for item in chosen])
        try:
            params_float = np.linalg.solve(matrix_float, rhs_float)
        except np.linalg.LinAlgError:
            singular_combinations += 1
            continue

        values_float = particular_float + basis_float.dot(params_float)
        if values_float.min() < lo - 1e-8 or values_float.max() > hi + 1e-8:
            continue

        feasible_combinations += 1
        params = base.solve_unique_system(
            [item["coeff_exact"] for item in chosen],
            [item["rhs_exact"] for item in chosen],
            dimension,
        )
        if params is None:
            continue

        candidate = tuple(
            particular[idx] + sum(params[k] * basis[k][idx] for k in range(dimension))
            for idx in range(variable_count)
        )
        if not base.is_feasible_fixed_square(candidate, n, magic_sum, lo, hi):
            continue

        exact_feasible_combinations += 1
        square = base.vector_to_square(candidate, n)
        active = base.active_bounds_for_fraction_square(square, lo, hi)
        vertices.setdefault(
            candidate,
            {
                "matrix": base.square_fraction_json(square),
                "active_bound_count": len(active),
                "active_bounds": active,
            },
        )

    sorted_vertices = sorted(
        vertices.values(), key=lambda row: json.dumps(row["matrix"], sort_keys=True)
    )
    sorted_vertex_vectors = [
        flatten_square(vertex["matrix"]) for vertex in sorted_vertices
    ]
    vertex_set = set(sorted_vertex_vectors)

    max_denominator_distribution = Counter(
        max(value.denominator for value in vertex) for vertex in vertex_set
    )
    active_bound_count_distribution = Counter(
        vertex["active_bound_count"] for vertex in sorted_vertices
    )
    integral_vertex_count = max_denominator_distribution[1]

    d10_vector = tuple(Fraction(x) for row in base.durer_ray_square(10) for x in row)
    local_face = base.enumerate_fixed_sum_face_vertices()
    local_vertex_vectors = [flatten_square(vertex["matrix"]) for vertex in local_face["vertices"]]
    local_subset = all(vertex in vertex_set for vertex in local_vertex_vectors)

    full_index_by_vertex = {vertex: idx for idx, vertex in enumerate(sorted_vertex_vectors)}
    barycentric = base.local_face_barycentric_certificate()
    local_bary_vertices = [
        flatten_square(vertex["matrix"]) for vertex in barycentric["vertices"]
    ]
    full_bary_indices = [full_index_by_vertex[vertex] for vertex in local_bary_vertices]

    vertex_squares = [
        base.square_from_fraction_json(vertex["matrix"]) for vertex in sorted_vertices
    ]
    stabilizer = []
    for name in base.d4_cell_transforms(n):
        image_set = {
            tuple(x for row in base.transform_square(square, name) for x in row)
            for square in vertex_squares
        }
        if image_set == vertex_set:
            stabilizer.append(name)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase E",
            "description": "Full vertex audit of the fixed-sum S=24 bounded order-4 magic polytope.",
            "method": "Float filter plus exact rational reconstruction/verification.",
        },
        "polytope": {
            "order": 4,
            "fixed_sum": magic_sum,
            "lower_bound": lo,
            "upper_bound": hi,
            "affine_dimension": dimension,
            "vertex_count": len(sorted_vertices),
            "integral_vertex_count": integral_vertex_count,
            "semi_integral_vertex_count": len(sorted_vertices) - integral_vertex_count,
            "max_denominator_distribution": {
                str(k): max_denominator_distribution[k]
                for k in sorted(max_denominator_distribution)
            },
            "active_bound_count_distribution": {
                str(k): active_bound_count_distribution[k]
                for k in sorted(active_bound_count_distribution)
            },
            "D4_square_symmetry_stabilizer": stabilizer,
            "D4_square_symmetry_stabilizer_size": len(stabilizer),
        },
        "enumeration": {
            "bound_hyperplane_count": len(hyperplanes),
            "checked_combinations": checked_combinations,
            "singular_combinations": singular_combinations,
            "float_feasible_combinations": feasible_combinations,
            "exact_feasible_combinations": exact_feasible_combinations,
        },
        "D10": {
            "is_vertex": d10_vector in vertex_set,
            "minimal_face_vertex_count": local_face["vertex_count"],
            "minimal_face_is_subset_of_full_polytope_vertices": local_subset,
            "local_barycentric_vertex_indices": barycentric["vertex_indices"],
            "full_barycentric_vertex_indices": full_bary_indices,
            "barycentric_weights": barycentric["weights"],
        },
        "vertices": sorted_vertices,
    }


def write_report(result: dict[str, Any]) -> None:
    path = ROOT / "results" / "FIXED_SUM24_POLYTOPE_AUDIT_REPORT.md"
    p = result["polytope"]
    d10 = result["D10"]
    enum = result["enumeration"]
    lines = [
        "# Fixed-Sum S=24 Polytope Audit",
        "",
        "Status: Phase E full fixed-sum vertex audit",
        "",
        "## Polytope",
        "",
        "```text",
        f"affine dimension: {p['affine_dimension']}",
        f"vertex count: {p['vertex_count']}",
        f"integral vertices: {p['integral_vertex_count']}",
        f"semi-integral vertices: {p['semi_integral_vertex_count']}",
        f"max denominator distribution: {p['max_denominator_distribution']}",
        f"active-bound count distribution: {p['active_bound_count_distribution']}",
        f"D4 square-symmetry stabilizer: {p['D4_square_symmetry_stabilizer']}",
        "```",
        "",
        "## D(10)",
        "",
        "```text",
        f"is vertex of full S=24 polytope: {d10['is_vertex']}",
        f"minimal local face vertices: {d10['minimal_face_vertex_count']}",
        f"local face vertices are full-polytope vertices: {d10['minimal_face_is_subset_of_full_polytope_vertices']}",
        f"local barycentric vertices: {d10['local_barycentric_vertex_indices']}",
        f"full barycentric vertices: {d10['full_barycentric_vertex_indices']}",
        f"barycentric weights: {d10['barycentric_weights']}",
        "```",
        "",
        "## Enumeration Audit",
        "",
        "```text",
        f"bound hyperplanes: {enum['bound_hyperplane_count']}",
        f"checked combinations: {enum['checked_combinations']}",
        f"singular combinations: {enum['singular_combinations']}",
        f"float-feasible combinations: {enum['float_feasible_combinations']}",
        f"exact-feasible combinations: {enum['exact_feasible_combinations']}",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = audit_fixed_sum24_polytope()
    if args.write:
        path = ROOT / "results" / "fixed_sum24_polytope_audit.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        write_report(result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
