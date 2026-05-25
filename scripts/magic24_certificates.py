"""Exact finite certificates for the Magic 24 project.

This script intentionally uses only the Python standard library.  It is the
first replay layer for the claims in `nota_24_meet_lo_shu_durer.md`.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


DURER_COMPLEMENT = (
    (1, 14, 15, 4),
    (12, 7, 6, 9),
    (8, 11, 10, 5),
    (13, 2, 3, 16),
)

SAGRADA_MASK_PERM = (2, 0, 1, 3)


def perm_string(p: tuple[int, ...]) -> str:
    return "".join(str(x) for x in p)


def matrix_to_lists(m: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    return [list(row) for row in m]


def lo_shu_param_matrix(g: int, a: int, b: int) -> tuple[tuple[int, ...], ...]:
    return (
        (g + a, g - a - b, g + b),
        (g - a + b, g, g + a - b),
        (g - b, g + a + b, g - a),
    )


def is_bounded_matrix(m: tuple[tuple[int, ...], ...], lo: int, hi: int) -> bool:
    return all(lo <= x <= hi for row in m for x in row)


def lo_shu_bounded_spectrum(bound: int = 9) -> dict:
    by_sum: dict[int, set[tuple[tuple[int, ...], ...]]] = {}
    for g in range(1, bound + 1):
        for a in range(-bound, bound + 1):
            for b in range(-bound, bound + 1):
                m = lo_shu_param_matrix(g, a, b)
                if is_bounded_matrix(m, 1, bound):
                    by_sum.setdefault(3 * g, set()).add(m)

    counts = {str(s): len(by_sum.get(s, set())) for s in range(3, 3 * bound + 1, 3)}
    upward = [s for s in sorted(by_sum) if s > 15]
    return {
        "bound": bound,
        "counts_by_sum": counts,
        "upward_spectrum_above_15": upward,
        "s24_matrices": [matrix_to_lists(m) for m in sorted(by_sum[24])],
        "s27_matrices": [matrix_to_lists(m) for m in sorted(by_sum[27])],
    }


def d_value(i: int, j: int) -> int:
    return DURER_COMPLEMENT[i][j]


def touched_values(p: tuple[int, ...]) -> list[int]:
    return [d_value(i, p[i]) for i in range(4)]


def is_one_incidence_mask(p: tuple[int, ...]) -> bool:
    main = sum(1 for i, j in enumerate(p) if i == j)
    anti = sum(1 for i, j in enumerate(p) if i + j == 3)
    return main == 1 and anti == 1


def durer_one_incidence_masks() -> dict:
    rows = []
    for p in itertools.permutations(range(4)):
        if not is_one_incidence_mask(p):
            continue
        values = touched_values(p)
        t_max = min(v - 1 for v in values)
        rows.append(
            {
                "perm": perm_string(p),
                "values": values,
                "t_max": t_max,
                "terminal_sum": 34 - t_max,
                "is_sagrada": p == SAGRADA_MASK_PERM,
            }
        )
    rows.sort(key=lambda r: r["perm"])
    terminal_24 = [r["perm"] for r in rows if r["terminal_sum"] == 24]
    return {
        "admissible_count": len(rows),
        "masks": rows,
        "terminal_24_masks": terminal_24,
    }


def mask_incidence(cells: Iterable[tuple[int, int]], mask_perm=SAGRADA_MASK_PERM) -> int:
    return sum(1 for i, j in cells if mask_perm[i] == j)


def durer_t_value(i: int, j: int, t: int, mask_perm=SAGRADA_MASK_PERM) -> int:
    return d_value(i, j) - (t if mask_perm[i] == j else 0)


def all_cells() -> list[tuple[int, int]]:
    return [(i, j) for i in range(4) for j in range(4)]


def encode_cells(cells: Iterable[tuple[int, int]]) -> list[str]:
    return [f"{i},{j}" for i, j in cells]


def durer_pattern_transport() -> dict:
    cells = all_cells()
    quads = list(itertools.combinations(cells, 4))

    h34 = [q for q in quads if sum(d_value(i, j) for i, j in q) == 34]
    incidence_distribution = Counter(mask_incidence(q) for q in h34)

    d10_h24 = [q for q in quads if sum(durer_t_value(i, j, 10) for i, j in q) == 24]
    source_decomposition = Counter(
        (sum(d_value(i, j) for i, j in q), mask_incidence(q)) for q in d10_h24
    )

    return {
        "h34_count": len(h34),
        "h34_incidence_distribution": {
            str(k): incidence_distribution.get(k, 0) for k in sorted(incidence_distribution)
        },
        "d10_h24_count": len(d10_h24),
        "d10_h24_source_decomposition": {
            f"source_sum_{s}_incidence_{inc}": count
            for (s, inc), count in sorted(source_decomposition.items())
        },
        "h34_quaternes": [encode_cells(q) for q in h34],
        "d10_h24_quaternes": [encode_cells(q) for q in d10_h24],
    }


def perm_parity(p: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return inv % 2


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def is_subgroup(perms: set[tuple[int, ...]]) -> bool:
    ident = tuple(range(4))
    if ident not in perms:
        return False
    for p in perms:
        if inverse(p) not in perms:
            return False
        for q in perms:
            if compose(p, q) not in perms:
                return False
    return True


def perm_order(p: tuple[int, ...]) -> int:
    ident = tuple(range(len(p)))
    current = ident
    for k in range(1, 25):
        current = compose(p, current)
        if current == ident:
            return k
    raise ValueError(f"order search exceeded bound for {p!r}")


def order_profile(perms: set[tuple[int, ...]]) -> dict[str, int]:
    counts = Counter(perm_order(p) for p in perms)
    return {str(k): counts[k] for k in sorted(counts)}


def left_cosets(subgroup: set[tuple[int, ...]]) -> list[list[str]]:
    all_perms = set(itertools.permutations(range(4)))
    remaining = set(all_perms)
    cosets = []
    while remaining:
        g = min(remaining)
        coset = {compose(g, h) for h in subgroup}
        cosets.append([perm_string(p) for p in sorted(coset)])
        remaining -= coset
    return cosets


def perm_diagonal_sum(p: tuple[int, ...], t: int = 0) -> int:
    return sum(durer_t_value(i, p[i], t) for i in range(4))


def common_precedence_relations(words: Iterable[tuple[int, ...]]) -> list[str]:
    words = list(words)
    relations = []
    for a in range(4):
        for b in range(4):
            if a == b:
                continue
            if all(w.index(a) < w.index(b) for w in words):
                relations.append(f"{a}<{b}")
    return sorted(relations)


def closure_size_from_common_relations(words: Iterable[tuple[int, ...]]) -> int:
    relations = common_precedence_relations(words)
    pairs = [(int(r[0]), int(r[2])) for r in relations]
    count = 0
    for p in itertools.permutations(range(4)):
        if all(p.index(a) < p.index(b) for a, b in pairs):
            count += 1
    return count


def durer_permutation_diagonals() -> dict:
    all_perms = list(itertools.permutations(range(4)))
    target_by_t = {}
    for t in range(0, 11):
        target = 34 - t
        group = {p for p in all_perms if perm_diagonal_sum(p, t) == target}
        target_by_t[str(t)] = [perm_string(p) for p in sorted(group)]

    g34 = {tuple(int(c) for c in s) for s in target_by_t["0"]}
    v4 = {tuple(int(c) for c in s) for s in target_by_t["1"]}

    return {
        "target_diagonals_by_t": target_by_t,
        "g34_is_subgroup": is_subgroup(g34),
        "v4_is_subgroup": is_subgroup(v4),
        "g34_order_profile": order_profile(g34),
        "v4_order_profile": order_profile(v4),
        "g34_left_cosets": left_cosets(g34),
        "v4_left_cosets": left_cosets(v4),
        "poset_cone_tests": {
            "G34": {
                "common_precedence_relations": common_precedence_relations(g34),
                "common_halfspace_closure_size": closure_size_from_common_relations(g34),
                "is_standard_poset_cone": closure_size_from_common_relations(g34) == len(g34),
            },
            "V4": {
                "common_precedence_relations": common_precedence_relations(v4),
                "common_halfspace_closure_size": closure_size_from_common_relations(v4),
                "is_standard_poset_cone": closure_size_from_common_relations(v4) == len(v4),
            },
        },
    }


def poly_add(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return trim_poly(out)


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return trim_poly(out)


def poly_pow_linear(const: int, t_coeff: int, k: int) -> list[int]:
    out = [1]
    base = [const, t_coeff]
    for _ in range(k):
        out = poly_mul(out, base)
    return out


def trim_poly(p: list[int]) -> list[int]:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def apd_polynomial(k: int) -> list[int]:
    coeffs = [0]
    for p in itertools.permutations(range(4)):
        base = sum(d_value(i, p[i]) for i in range(4))
        inc = sum(1 for i in range(4) if p[i] == SAGRADA_MASK_PERM[i])
        term = poly_pow_linear(base, -inc, k)
        if perm_parity(p) == 0:
            coeffs = poly_add(coeffs, term)
        else:
            coeffs = poly_add(coeffs, [-x for x in term])
    return trim_poly(coeffs)


def determinant_3x3_poly(m: list[list[list[int]]]) -> list[int]:
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    positive = poly_add(poly_add(poly_mul(poly_mul(a, e), i), poly_mul(poly_mul(b, f), g)), poly_mul(poly_mul(c, d), h))
    negative = poly_add(poly_add(poly_mul(poly_mul(c, e), g), poly_mul(poly_mul(b, d), i)), poly_mul(poly_mul(a, f), h))
    return trim_poly(poly_add(positive, [-x for x in negative]))


def centered_ray_polynomials() -> dict:
    # Entries are polynomials in t, represented by ascending coefficients.
    ehat = [
        [[0, -1], [24, -1], [24, -2]],
        [[6, -2], [12, -1], [10, -1]],
        [[6, -1], [20, -2], [18, -1]],
    ]
    det = determinant_3x3_poly(ehat)
    apd = {str(k): apd_polynomial(k) for k in range(1, 5)}
    apd3_equals_6_det = apd["3"] == [6 * c for c in det]
    return {
        "apd_coefficients_ascending": apd,
        "det_ehat_coefficients_ascending": det,
        "apd3_equals_6_det_ehat": apd3_equals_6_det,
    }


def build_certificate() -> dict:
    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Exact finite replay for the Lo Shu / Durer 24-meet.",
            "indexing": "All matrix and cell indices are zero-based in generated data.",
        },
        "lo_shu_bounded_spectrum": lo_shu_bounded_spectrum(),
        "durer_one_incidence_masks": durer_one_incidence_masks(),
        "durer_pattern_transport": durer_pattern_transport(),
        "durer_permutation_diagonals": durer_permutation_diagonals(),
        "apd_centered_ray": centered_ray_polynomials(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write JSON certificate into results/")
    args = parser.parse_args()

    cert = build_certificate()
    text = json.dumps(cert, indent=2, sort_keys=True)

    if args.write:
        root = Path(__file__).resolve().parents[1]
        out = root / "results" / "magic24_certificate_pack.json"
        out.write_text(text + "\n", encoding="utf-8")
        print(out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
