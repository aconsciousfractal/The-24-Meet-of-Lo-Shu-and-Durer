"""Phase-E bounded magic-polytope checks for Magic 24.

This script keeps the first polytope layer deliberately elementary:

- ranks of the free-sum and fixed-sum magic affine spaces;
- active box facets along the Durer/Sagrada ray;
- local face dimensions at D(0) and D(10);
- the Lo Shu S=24 fiber as a 2D lattice polygon in the (a,b) parameters.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAGIC24_SCRIPT = ROOT / "scripts" / "magic24_certificates.py"

spec = importlib.util.spec_from_file_location("magic24_certificates", MAGIC24_SCRIPT)
magic24 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(magic24)


def matrix_to_lists(m: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    return [list(row) for row in m]


def cell_label(i: int, j: int) -> str:
    return f"r{i}c{j}"


def rational_rank(rows: list[list[int | Fraction]]) -> int:
    """Rank over Q by Gaussian elimination."""
    mat = [[Fraction(x) for x in row] for row in rows if any(x != 0 for x in row)]
    if not mat:
        return 0
    m = len(mat)
    n = len(mat[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = None
        for r in range(rank, m):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pv = mat[rank][col]
        mat[rank] = [x / pv for x in mat[rank]]
        for r in range(m):
            if r != rank and mat[r][col] != 0:
                factor = mat[r][col]
                mat[r] = [mat[r][c] - factor * mat[rank][c] for c in range(n)]
        rank += 1
        col += 1
    return rank


def line_vectors(n: int) -> list[list[int]]:
    vectors = []
    for i in range(n):
        row = [0] * (n * n)
        for j in range(n):
            row[i * n + j] = 1
        vectors.append(row)
    for j in range(n):
        col = [0] * (n * n)
        for i in range(n):
            col[i * n + j] = 1
        vectors.append(col)
    main = [0] * (n * n)
    anti = [0] * (n * n)
    for i in range(n):
        main[i * n + i] = 1
        anti[i * n + (n - 1 - i)] = 1
    vectors.extend([main, anti])
    return vectors


def free_magic_equations(n: int) -> list[list[int]]:
    lines = line_vectors(n)
    base = lines[0]
    return [[line[k] - base[k] for k in range(n * n)] for line in lines[1:]]


def fixed_magic_equations(n: int) -> list[list[int]]:
    return line_vectors(n)


def fixed_magic_rhs(n: int, magic_sum: int) -> list[int]:
    return [magic_sum] * (2 * n + 2)


def affine_space_summary(n: int) -> dict[str, int]:
    free_eqs = free_magic_equations(n)
    fixed_eqs = fixed_magic_equations(n)
    free_rank = rational_rank(free_eqs)
    fixed_rank = rational_rank(fixed_eqs)
    return {
        "n": n,
        "variable_count": n * n,
        "line_count": 2 * n + 2,
        "free_sum_rank": free_rank,
        "free_sum_dimension": n * n - free_rank,
        "fixed_sum_rank": fixed_rank,
        "fixed_sum_dimension": n * n - fixed_rank,
    }


def solve_unique_system(
    rows: list[list[int | Fraction]], rhs: list[int | Fraction], variable_count: int
) -> tuple[Fraction, ...] | None:
    """Solve a rational linear system when it has a unique solution."""
    mat = [
        [Fraction(x) for x in row] + [Fraction(b)]
        for row, b in zip(rows, rhs)
        if any(x != 0 for x in row) or b != 0
    ]
    if not mat:
        return None

    m = len(mat)
    n = variable_count
    rank = 0
    pivots: list[int] = []
    col = 0
    while rank < m and col < n:
        pivot = None
        for r in range(rank, m):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pv = mat[rank][col]
        mat[rank] = [x / pv for x in mat[rank]]
        for r in range(m):
            if r != rank and mat[r][col] != 0:
                factor = mat[r][col]
                mat[r] = [mat[r][c] - factor * mat[rank][c] for c in range(n + 1)]
        pivots.append(col)
        rank += 1
        col += 1

    for r in range(rank, m):
        if all(mat[r][c] == 0 for c in range(n)) and mat[r][n] != 0:
            return None
    if rank != n:
        return None

    solution = [Fraction(0) for _ in range(n)]
    for row_index, pivot_col in enumerate(pivots):
        solution[pivot_col] = mat[row_index][n]
    return tuple(solution)


def affine_solution_space(
    rows: list[list[int | Fraction]], rhs: list[int | Fraction], variable_count: int
) -> tuple[tuple[Fraction, ...], list[tuple[Fraction, ...]]] | None:
    """Return one solution and a basis for the nullspace of Ax=b."""
    mat = [
        [Fraction(x) for x in row] + [Fraction(b)]
        for row, b in zip(rows, rhs)
        if any(x != 0 for x in row) or b != 0
    ]
    if not mat:
        zero = tuple(Fraction(0) for _ in range(variable_count))
        basis = [
            tuple(Fraction(1 if i == j else 0) for i in range(variable_count))
            for j in range(variable_count)
        ]
        return zero, basis

    m = len(mat)
    n = variable_count
    rank = 0
    pivots: list[int] = []
    col = 0
    while rank < m and col < n:
        pivot = None
        for r in range(rank, m):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pv = mat[rank][col]
        mat[rank] = [x / pv for x in mat[rank]]
        for r in range(m):
            if r != rank and mat[r][col] != 0:
                factor = mat[r][col]
                mat[r] = [mat[r][c] - factor * mat[rank][c] for c in range(n + 1)]
        pivots.append(col)
        rank += 1
        col += 1

    for r in range(rank, m):
        if all(mat[r][c] == 0 for c in range(n)) and mat[r][n] != 0:
            return None

    free_cols = [c for c in range(n) if c not in pivots]
    particular = [Fraction(0) for _ in range(n)]
    for row_index, pivot_col in enumerate(pivots):
        particular[pivot_col] = mat[row_index][n]

    basis = []
    for free_col in free_cols:
        vec = [Fraction(0) for _ in range(n)]
        vec[free_col] = Fraction(1)
        for row_index, pivot_col in enumerate(pivots):
            vec[pivot_col] = -mat[row_index][free_col]
        basis.append(tuple(vec))
    return tuple(particular), basis


def active_bounds(
    square: tuple[tuple[int, ...], ...], lo: int, hi: int
) -> list[dict[str, Any]]:
    out = []
    for i, row in enumerate(square):
        for j, value in enumerate(row):
            if value == lo or value == hi:
                out.append(
                    {
                        "cell": [i, j],
                        "label": cell_label(i, j),
                        "value": value,
                        "bound": "lower" if value == lo else "upper",
                    }
                )
    return out


def active_unit_rows(n: int, active: list[dict[str, Any]]) -> list[list[int]]:
    rows = []
    for item in active:
        i, j = item["cell"]
        row = [0] * (n * n)
        row[i * n + j] = 1
        rows.append(row)
    return rows


def unit_row(n: int, i: int, j: int) -> list[int]:
    row = [0] * (n * n)
    row[i * n + j] = 1
    return row


def face_summary(
    square: tuple[tuple[int, ...], ...],
    lo: int,
    hi: int,
    fixed_sum: int | None,
) -> dict[str, Any]:
    n = len(square)
    active = active_bounds(square, lo, hi)
    eqs = fixed_magic_equations(n) if fixed_sum is not None else free_magic_equations(n)
    combined_rank = rational_rank(eqs + active_unit_rows(n, active))
    base_rank = rational_rank(eqs)
    dimension = n * n - combined_rank
    return {
        "fixed_sum": fixed_sum,
        "base_rank": base_rank,
        "base_dimension": n * n - base_rank,
        "active_bound_count": len(active),
        "active_bounds": active,
        "face_dimension": dimension,
        "is_vertex": dimension == 0,
    }


def vector_to_square(v: tuple[Fraction, ...], n: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(v[i * n + j] for j in range(n)) for i in range(n))


def fraction_json(x: Fraction) -> int | str:
    if x.denominator == 1:
        return int(x)
    return f"{x.numerator}/{x.denominator}"


def square_fraction_json(square: tuple[tuple[Fraction, ...], ...]) -> list[list[int | str]]:
    return [[fraction_json(x) for x in row] for row in square]


def square_from_fraction_json(matrix: list[list[int | str]]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(Fraction(x) for x in row) for row in matrix)


def is_feasible_fixed_square(
    v: tuple[Fraction, ...], n: int, magic_sum: int, lo: int, hi: int
) -> bool:
    if not all(Fraction(lo) <= x <= Fraction(hi) for x in v):
        return False
    square = vector_to_square(v, n)
    return (
        all(sum(row) == magic_sum for row in square)
        and all(sum(square[i][j] for i in range(n)) == magic_sum for j in range(n))
        and sum(square[i][i] for i in range(n)) == magic_sum
        and sum(square[i][n - 1 - i] for i in range(n)) == magic_sum
    )


def active_bounds_for_fraction_square(
    square: tuple[tuple[Fraction, ...], ...], lo: int, hi: int
) -> list[dict[str, Any]]:
    out = []
    for i, row in enumerate(square):
        for j, value in enumerate(row):
            if value == lo or value == hi:
                out.append(
                    {
                        "cell": [i, j],
                        "label": cell_label(i, j),
                        "value": fraction_json(value),
                        "bound": "lower" if value == lo else "upper",
                    }
                )
    return out


def d4_cell_transforms(n: int = 4) -> dict[str, Any]:
    return {
        "id": lambda i, j: (i, j),
        "rot90": lambda i, j: (j, n - 1 - i),
        "rot180": lambda i, j: (n - 1 - i, n - 1 - j),
        "rot270": lambda i, j: (n - 1 - j, i),
        "ref_main_diag": lambda i, j: (j, i),
        "ref_anti_diag": lambda i, j: (n - 1 - j, n - 1 - i),
        "ref_vertical": lambda i, j: (i, n - 1 - j),
        "ref_horizontal": lambda i, j: (n - 1 - i, j),
    }


def transform_square(
    square: tuple[tuple[Fraction, ...], ...], transform_name: str
) -> tuple[tuple[Fraction, ...], ...]:
    n = len(square)
    fn = d4_cell_transforms(n)[transform_name]
    out = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            ni, nj = fn(i, j)
            out[ni][nj] = square[i][j]
    return tuple(tuple(row) for row in out)


def durer_ray_square(t: int) -> tuple[tuple[int, ...], ...]:
    mask = magic24.SAGRADA_MASK_PERM
    return tuple(
        tuple(
            magic24.DURER_COMPLEMENT[i][j] - (t if mask[i] == j else 0)
            for j in range(4)
        )
        for i in range(4)
    )


@lru_cache(maxsize=4)
def enumerate_fixed_sum_face_vertices(
    magic_sum: int = 24,
    lo: int = 1,
    hi: int = 16,
    forced_bounds: tuple[tuple[int, int, int], ...] = ((0, 0, 1), (2, 1, 1)),
) -> dict[str, Any]:
    """Enumerate vertices of the fixed-sum face containing D(10)."""
    n = 4
    variable_count = n * n
    base_rows = fixed_magic_equations(n)
    base_rhs = fixed_magic_rhs(n, magic_sum)
    forced_rows = [unit_row(n, i, j) for i, j, _ in forced_bounds]
    forced_rhs = [value for _, _, value in forced_bounds]
    affine = affine_solution_space(
        list(base_rows) + list(forced_rows),
        list(base_rhs) + list(forced_rhs),
        variable_count,
    )
    if affine is None:
        raise ValueError("forced face is empty")
    particular, basis = affine
    parameter_count = len(basis)

    forced_cells = {(i, j) for i, j, _ in forced_bounds}
    bound_hyperplanes = []
    for i in range(n):
        for j in range(n):
            if (i, j) in forced_cells:
                continue
            idx = i * n + j
            coeffs = [vec[idx] for vec in basis]
            for value in (lo, hi):
                bound_hyperplanes.append((idx, value, coeffs, Fraction(value) - particular[idx]))

    vertices: dict[tuple[Fraction, ...], dict[str, Any]] = {}
    for chosen in itertools.combinations(bound_hyperplanes, parameter_count):
        rows = [list(item[2]) for item in chosen]
        rhs = [item[3] for item in chosen]
        params = solve_unique_system(rows, rhs, parameter_count)
        if params is None:
            continue
        solution = tuple(
            particular[idx]
            + sum(params[k] * basis[k][idx] for k in range(parameter_count))
            for idx in range(variable_count)
        )
        if not is_feasible_fixed_square(solution, n, magic_sum, lo, hi):
            continue
        if any(solution[i * n + j] != value for i, j, value in forced_bounds):
            continue
        square = vector_to_square(solution, n)
        active = active_bounds_for_fraction_square(square, lo, hi)
        vertices.setdefault(
            solution,
            {
                "matrix": square_fraction_json(square),
                "active_bound_count": len(active),
                "active_bounds": active,
            },
        )

    d10_vector = tuple(Fraction(x) for row in durer_ray_square(10) for x in row)
    denominator_counts: dict[str, int] = {}
    active_counts: dict[str, int] = {}
    integral_count = 0
    for vertex, row in vertices.items():
        max_den = max(x.denominator for x in vertex)
        denominator_counts[str(max_den)] = denominator_counts.get(str(max_den), 0) + 1
        if max_den == 1:
            integral_count += 1
        active_count = row["active_bound_count"]
        active_counts[str(active_count)] = active_counts.get(str(active_count), 0) + 1

    sorted_vertices = sorted(
        vertices.values(), key=lambda row: json.dumps(row["matrix"], sort_keys=True)
    )
    return {
        "fixed_sum": magic_sum,
        "forced_bounds": [
            {"cell": [i, j], "label": cell_label(i, j), "value": value}
            for i, j, value in forced_bounds
        ],
        "face_dimension": face_summary(durer_ray_square(10), lo, hi, magic_sum)[
            "face_dimension"
        ],
        "vertex_count": len(vertices),
        "integral_vertex_count": integral_count,
        "max_denominator_distribution": dict(sorted(denominator_counts.items())),
        "active_bound_count_distribution": dict(sorted(active_counts.items())),
        "D10_is_vertex_of_this_face": d10_vector in vertices,
        "vertices": sorted_vertices,
    }


def local_face_fingerprint() -> dict[str, Any]:
    face = enumerate_fixed_sum_face_vertices()
    n = 4
    vertex_squares = [
        square_from_fraction_json(vertex["matrix"]) for vertex in face["vertices"]
    ]
    vertex_set = {tuple(x for row in square for x in row) for square in vertex_squares}

    common_active = []
    for i in range(n):
        for j in range(n):
            values = {square[i][j] for square in vertex_squares}
            if values == {Fraction(1)}:
                common_active.append(
                    {"cell": [i, j], "label": cell_label(i, j), "value": 1}
                )
            elif values == {Fraction(16)}:
                common_active.append(
                    {"cell": [i, j], "label": cell_label(i, j), "value": 16}
                )

    stabilizer = []
    for name in d4_cell_transforms(n):
        image_set = {
            tuple(x for row in transform_square(square, name) for x in row)
            for square in vertex_squares
        }
        if image_set == vertex_set:
            stabilizer.append(name)

    d10 = tuple(tuple(Fraction(x) for x in row) for row in durer_ray_square(10))
    d10_active = active_bounds_for_fraction_square(d10, 1, 16)
    common_labels = {(item["label"], item["value"]) for item in common_active}
    d10_labels = {(item["label"], item["value"]) for item in d10_active}
    nonforced_values = [
        d10[i][j]
        for i in range(n)
        for j in range(n)
        if (cell_label(i, j), fraction_json(d10[i][j])) not in d10_labels
    ]
    lower_slacks = [value - 1 for value in nonforced_values]
    upper_slacks = [16 - value for value in nonforced_values]

    return {
        "common_active_bounds_across_vertices": common_active,
        "D4_vertex_set_stabilizer": stabilizer,
        "D4_vertex_set_stabilizer_size": len(stabilizer),
        "D10_active_bounds": d10_active,
        "D10_active_bounds_equal_common_active_bounds": d10_labels == common_labels,
        "D10_relative_interior_of_minimal_face": d10_labels == common_labels,
        "D10_nonforced_min_lower_slack": fraction_json(min(lower_slacks)),
        "D10_nonforced_min_upper_slack": fraction_json(min(upper_slacks)),
    }


def local_face_barycentric_certificate() -> dict[str, Any]:
    face = enumerate_fixed_sum_face_vertices()
    vertices = [
        tuple(Fraction(x) for row in vertex["matrix"] for x in row)
        for vertex in face["vertices"]
    ]
    d10 = tuple(Fraction(x) for row in durer_ray_square(10) for x in row)

    for i, j in itertools.combinations(range(len(vertices)), 2):
        rows = [[Fraction(1), Fraction(1)]]
        rhs = [Fraction(1)]
        for coord in range(16):
            rows.append([vertices[i][coord], vertices[j][coord]])
            rhs.append(d10[coord])
        weights = solve_unique_system(rows, rhs, 2)
        if weights is None or not all(weight > 0 for weight in weights):
            continue
        reconstructed = tuple(
            weights[0] * vertices[i][coord] + weights[1] * vertices[j][coord]
            for coord in range(16)
        )
        if reconstructed != d10:
            continue
        return {
            "type": "two_vertex_segment",
            "vertex_indices": [i, j],
            "weights": [fraction_json(weight) for weight in weights],
            "weights_sum": fraction_json(sum(weights)),
            "strictly_positive_weights": all(weight > 0 for weight in weights),
            "reconstructs_D10": True,
            "vertices": [
                {
                    "index": i,
                    "matrix": face["vertices"][i]["matrix"],
                    "active_bounds": face["vertices"][i]["active_bounds"],
                },
                {
                    "index": j,
                    "matrix": face["vertices"][j]["matrix"],
                    "active_bounds": face["vertices"][j]["active_bounds"],
                },
            ],
        }

    raise ValueError("no two-vertex barycentric certificate found")


def line_sums(square: tuple[tuple[int, ...], ...]) -> dict[str, list[int]]:
    n = len(square)
    return {
        "rows": [sum(row) for row in square],
        "columns": [sum(square[i][j] for i in range(n)) for j in range(n)],
        "diagonals": [
            sum(square[i][i] for i in range(n)),
            sum(square[i][n - 1 - i] for i in range(n)),
        ],
    }


def sagrada_ray_summary() -> dict[str, Any]:
    selected = [
        {
            "cell": [i, magic24.SAGRADA_MASK_PERM[i]],
            "label": cell_label(i, magic24.SAGRADA_MASK_PERM[i]),
            "source_value": magic24.DURER_COMPLEMENT[i][magic24.SAGRADA_MASK_PERM[i]],
        }
        for i in range(4)
    ]
    terminal_t = min(item["source_value"] - 1 for item in selected)
    terminal_cells = [
        item for item in selected if item["source_value"] - terminal_t == 1
    ]

    start = durer_ray_square(0)
    terminal = durer_ray_square(terminal_t)
    interior = durer_ray_square(1)

    ray_active = {
        "t_0": active_bounds(start, 1, 16),
        "t_1_to_9_constant": active_bounds(interior, 1, 16),
        "t_10": active_bounds(terminal, 1, 16),
    }

    return {
        "mask": magic24.perm_string(magic24.SAGRADA_MASK_PERM),
        "selected_cells": selected,
        "t_interval_downward": [0, terminal_t],
        "terminal_t": terminal_t,
        "source_magic_sum": line_sums(start)["rows"][0],
        "terminal_magic_sum": line_sums(terminal)["rows"][0],
        "terminal_hit_cells": terminal_cells,
        "active_bounds_along_ray": ray_active,
        "D0": {
            "matrix": matrix_to_lists(start),
            "line_sums": line_sums(start),
            "free_sum_face": face_summary(start, 1, 16, None),
            "fixed_sum_face": face_summary(start, 1, 16, 34),
        },
        "D10": {
            "matrix": matrix_to_lists(terminal),
            "line_sums": line_sums(terminal),
            "free_sum_face": face_summary(terminal, 1, 16, None),
            "fixed_sum_face": face_summary(terminal, 1, 16, 24),
        },
    }


LO_SHU_AB_COEFFS = (
    (1, 0),
    (-1, -1),
    (0, 1),
    (-1, 1),
    (0, 0),
    (1, -1),
    (0, -1),
    (1, 1),
    (-1, 0),
)


def lo_shu_inequalities(g: int, lo: int = 1, hi: int = 9) -> list[tuple[int, int, int]]:
    """Return inequalities A*a + B*b <= C for the fixed center g."""
    inequalities = []
    for ca, cb in LO_SHU_AB_COEFFS:
        inequalities.append((ca, cb, hi - g))
        inequalities.append((-ca, -cb, g - lo))
    # Remove all-zero constraints from the center cell.
    return [ineq for ineq in inequalities if ineq[0] != 0 or ineq[1] != 0]


def satisfies_ineq(point: tuple[Fraction, Fraction], ineq: tuple[int, int, int]) -> bool:
    a, b = point
    A, B, C = ineq
    return A * a + B * b <= C


def lo_shu_polygon_vertices(g: int) -> list[tuple[Fraction, Fraction]]:
    inequalities = lo_shu_inequalities(g)
    vertices: set[tuple[Fraction, Fraction]] = set()
    for left, right in itertools.combinations(inequalities, 2):
        A1, B1, C1 = left
        A2, B2, C2 = right
        det = A1 * B2 - A2 * B1
        if det == 0:
            continue
        a = Fraction(C1 * B2 - C2 * B1, det)
        b = Fraction(A1 * C2 - A2 * C1, det)
        p = (a, b)
        if all(satisfies_ineq(p, ineq) for ineq in inequalities):
            vertices.add(p)
    if not vertices:
        return []
    center_a = sum(v[0] for v in vertices) / len(vertices)
    center_b = sum(v[1] for v in vertices) / len(vertices)

    def angle_key(p: tuple[Fraction, Fraction]) -> float:
        # Sorting only; float is fine for deterministic display of tiny sets.
        import math

        return math.atan2(float(p[1] - center_b), float(p[0] - center_a))

    return sorted(vertices, key=angle_key)


def fraction_pair_to_lists(p: tuple[Fraction, Fraction]) -> list[str]:
    return [str(p[0]), str(p[1])]


def lo_shu_lattice_count(g: int) -> int:
    inequalities = lo_shu_inequalities(g)
    # The project bounds are tiny; this intentionally remains transparent.
    count = 0
    for a in range(-9, 10):
        for b in range(-9, 10):
            if all(satisfies_ineq((Fraction(a), Fraction(b)), ineq) for ineq in inequalities):
                count += 1
    return count


def lo_shu_common_active_bounds(g: int) -> list[str]:
    vertices = lo_shu_polygon_vertices(g)
    if not vertices:
        return []
    inequalities = lo_shu_inequalities(g)
    common = []
    for idx, ineq in enumerate(inequalities):
        A, B, C = ineq
        if all(A * a + B * b == C for a, b in vertices):
            common.append(f"ineq_{idx}:{A}a+{B}b<={C}")
    return common


def lo_shu_parametric_summary() -> dict[str, Any]:
    counts = {str(3 * g): lo_shu_lattice_count(g) for g in range(1, 10)}
    g = 8
    vertices = lo_shu_polygon_vertices(g)
    return {
        "model": "Lo Shu fixed-sum fiber uses center g=S/3 and integer parameters (a,b).",
        "counts_by_sum": counts,
        "s24": {
            "g": g,
            "dimension": 2 if len(vertices) >= 3 else len(vertices) - 1,
            "lattice_point_count": lo_shu_lattice_count(g),
            "vertices_ab": [fraction_pair_to_lists(v) for v in vertices],
            "common_active_bounds": lo_shu_common_active_bounds(g),
            "is_common_boundary_face_of_free_polytope": bool(lo_shu_common_active_bounds(g)),
        },
    }


def lo_shu_lattice_formula_summary() -> dict[str, Any]:
    rows = []
    for g in range(1, 10):
        m = min(g - 1, 9 - g)
        formula_count = 2 * m * m + 2 * m + 1
        measured_count = lo_shu_lattice_count(g)
        rows.append(
            {
                "g": g,
                "sum": 3 * g,
                "m": m,
                "vertices_ab": [[m, 0], [0, m], [-m, 0], [0, -m]]
                if m > 0
                else [[0, 0]],
                "area": 2 * m * m,
                "boundary_lattice_points": 4 * m if m > 0 else 1,
                "pick_formula_count": formula_count,
                "measured_lattice_count": measured_count,
                "matches_formula": measured_count == formula_count,
            }
        )
    return {
        "statement": "For fixed center g, put m=min(g-1,9-g). The bounded Lo Shu fiber is the lattice diamond |a+b|<=m, |a-b|<=m, with count 2m^2+2m+1.",
        "rows": rows,
        "all_counts_match_formula": all(row["matches_formula"] for row in rows),
        "counts_by_sum_formula": {str(row["sum"]): row["pick_formula_count"] for row in rows},
    }


def analyze() -> dict[str, Any]:
    ray = sagrada_ray_summary()
    lo_shu = lo_shu_parametric_summary()
    lo_shu_formula = lo_shu_lattice_formula_summary()
    local_face = enumerate_fixed_sum_face_vertices()
    local_fingerprint = local_face_fingerprint()
    barycentric = local_face_barycentric_certificate()
    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase E",
            "description": "Initial bounded magic-polytope checks for the Sagrada ray and Lo Shu S=24 fiber.",
        },
        "affine_spaces": {
            "order3": affine_space_summary(3),
            "order4": affine_space_summary(4),
        },
        "sagrada_ray": ray,
        "lo_shu": lo_shu,
        "lo_shu_lattice_formula": lo_shu_formula,
        "D10_fixed_sum_24_minimal_face": local_face,
        "D10_fixed_sum_24_minimal_face_fingerprint": local_fingerprint,
        "D10_fixed_sum_24_barycentric_certificate": barycentric,
        "summary": {
            "D10_is_vertex_free_sum": ray["D10"]["free_sum_face"]["is_vertex"],
            "D10_is_vertex_fixed_sum_24": ray["D10"]["fixed_sum_face"]["is_vertex"],
            "D10_free_sum_face_dimension": ray["D10"]["free_sum_face"]["face_dimension"],
            "D10_fixed_sum_24_face_dimension": ray["D10"]["fixed_sum_face"][
                "face_dimension"
            ],
            "D10_fixed_sum_24_minimal_face_vertex_count": local_face["vertex_count"],
            "D10_fixed_sum_24_minimal_face_integral_vertex_count": local_face[
                "integral_vertex_count"
            ],
            "D10_local_face_D4_stabilizer_size": local_fingerprint[
                "D4_vertex_set_stabilizer_size"
            ],
            "D10_relative_interior_of_minimal_face": local_fingerprint[
                "D10_relative_interior_of_minimal_face"
            ],
            "D10_barycentric_certificate_type": barycentric["type"],
            "D10_barycentric_certificate_vertex_indices": barycentric[
                "vertex_indices"
            ],
            "D10_barycentric_certificate_weights": barycentric["weights"],
            "lo_shu_s24_lattice_count": lo_shu_lattice_count(8),
            "lo_shu_counts_match_lattice_formula": lo_shu_formula[
                "all_counts_match_formula"
            ],
        },
    }


def write_report(result: dict[str, Any]) -> None:
    path = ROOT / "results" / "BOUNDED_MAGIC_POLYTOPE_REPORT.md"
    ray = result["sagrada_ray"]
    lo = result["lo_shu"]["s24"]
    face = result["D10_fixed_sum_24_minimal_face"]
    fingerprint = result["D10_fixed_sum_24_minimal_face_fingerprint"]
    barycentric = result["D10_fixed_sum_24_barycentric_certificate"]
    lo_formula = result["lo_shu_lattice_formula"]
    lines = [
        "# Bounded Magic Polytope Report",
        "",
        "Status: Phase E initial linear certificate",
        "",
        "## Sagrada Ray",
        "",
        "```text",
        f"mask: {ray['mask']}",
        f"t interval: {ray['t_interval_downward']}",
        f"source sum: {ray['source_magic_sum']}",
        f"terminal sum: {ray['terminal_magic_sum']}",
        f"terminal hit cells: {[item['label'] for item in ray['terminal_hit_cells']]}",
        "```",
        "",
        "At `D(10)`:",
        "",
        "```text",
        f"free-sum face dimension: {ray['D10']['free_sum_face']['face_dimension']}",
        f"fixed-sum S=24 face dimension: {ray['D10']['fixed_sum_face']['face_dimension']}",
        f"vertex in free-sum polytope: {ray['D10']['free_sum_face']['is_vertex']}",
        f"vertex in fixed-sum S=24 polytope: {ray['D10']['fixed_sum_face']['is_vertex']}",
        "```",
        "",
        "Minimal fixed-sum `S=24` face containing `D(10)`:",
        "",
        "```text",
        f"forced bounds: {[item['label'] + '=' + str(item['value']) for item in face['forced_bounds']]}",
        f"face dimension: {face['face_dimension']}",
        f"vertex count: {face['vertex_count']}",
        f"integral vertices: {face['integral_vertex_count']}",
        f"D(10) is vertex of this face: {face['D10_is_vertex_of_this_face']}",
        f"max denominator distribution: {face['max_denominator_distribution']}",
        f"D4 stabilizer: {fingerprint['D4_vertex_set_stabilizer']}",
        f"D(10) relative interior: {fingerprint['D10_relative_interior_of_minimal_face']}",
        f"barycentric certificate: vertices {barycentric['vertex_indices']} with weights {barycentric['weights']}",
        "```",
        "",
        "## Lo Shu S=24 Fiber",
        "",
        "```text",
        f"g: {lo['g']}",
        f"dimension: {lo['dimension']}",
        f"lattice points: {lo['lattice_point_count']}",
        f"vertices (a,b): {lo['vertices_ab']}",
        f"common active bounds: {lo['common_active_bounds']}",
        "```",
        "",
        "Closed count formula:",
        "",
        "```text",
        "m = min(g-1, 9-g)",
        "|P_g cap Z^2| = 2m^2 + 2m + 1",
        f"counts by sum: {lo_formula['counts_by_sum_formula']}",
        f"all counts match formula: {lo_formula['all_counts_match_formula']}",
        "```",
        "",
        "## Reading",
        "",
        "- `D(10)` is a boundary point, not a vertex, of both the free-sum and",
        "  fixed-sum bounded order-4 magic polytopes.",
        "- The Sagrada ray lies on the persistent lower facet `r0c0 = 1`, leaves",
        "  the initial upper facet `r3c3 = 16`, and terminates when `r2c1 = 1`.",
        "- The Lo Shu `S=24` fiber has 5 lattice points in a 2D parameter polygon;",
        "  it is a bounded-slice phenomenon rather than a common boundary face.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = analyze()
    if args.write:
        path = ROOT / "results" / "bounded_magic_polytope.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        write_report(result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
