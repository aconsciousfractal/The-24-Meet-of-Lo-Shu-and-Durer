"""Internal order-4 normal magic-square dataset and endpoint spectrum.

The generator reconstructs all normal 4x4 magic squares with entries 1..16
and magic sum 34. It then canonicalizes by the 8 square symmetries, producing
the classical 880 essential representatives from the 7040 raw squares.

No external dataset is used.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path


MAGIC_SUM = 34
VALUES = tuple(range(1, 17))
FULL_MASK = (1 << 16) - 1


def value_mask(v: int) -> int:
    return 1 << (v - 1)


def row_mask(row: tuple[int, int, int, int]) -> int:
    mask = 0
    for v in row:
        mask |= value_mask(v)
    return mask


def matrix_to_flat(square: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(v for row in square for v in row)


def matrix_to_lists(square: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    return [list(row) for row in square]


@lru_cache(maxsize=1)
def row_candidates() -> tuple[tuple[tuple[int, int, int, int], int], ...]:
    rows = []
    for combo in itertools.combinations(VALUES, 4):
        if sum(combo) != MAGIC_SUM:
            continue
        for row in itertools.permutations(combo):
            rows.append((row, row_mask(row)))
    return tuple(rows)


@lru_cache(maxsize=1)
def rows_by_mask() -> dict[int, tuple[tuple[int, int, int, int], ...]]:
    grouped: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
    for row, mask in row_candidates():
        grouped[mask].append(row)
    return {mask: tuple(rows) for mask, rows in grouped.items()}


@lru_cache(maxsize=None)
def rows_disjoint_from(mask: int) -> tuple[tuple[tuple[int, int, int, int], int], ...]:
    return tuple((row, row_m) for row, row_m in row_candidates() if row_m & mask == 0)


@lru_cache(maxsize=1)
def lower_pair_map() -> dict[
    tuple[int, tuple[int, int, int, int], int, int],
    tuple[tuple[tuple[int, int, int, int], tuple[int, int, int, int]], ...],
]:
    """Map lower-row constraints to ordered row pairs.

    The key is:

    - used value mask of rows 2 and 3;
    - column sums contributed by rows 2 and 3;
    - main diagonal contribution r2[2] + r3[3];
    - anti-diagonal contribution r2[1] + r3[0].
    """
    grouped: dict[
        tuple[int, tuple[int, int, int, int], int, int],
        list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]],
    ] = defaultdict(list)
    for r2, m2 in row_candidates():
        for r3, m3 in rows_disjoint_from(m2):
            key = (
                m2 | m3,
                tuple(r2[j] + r3[j] for j in range(4)),
                r2[2] + r3[3],
                r2[1] + r3[0],
            )
            grouped[key].append((r2, r3))
    return {key: tuple(pairs) for key, pairs in grouped.items()}


def is_magic(square: tuple[tuple[int, ...], ...]) -> bool:
    if sorted(matrix_to_flat(square)) != list(VALUES):
        return False
    if any(sum(row) != MAGIC_SUM for row in square):
        return False
    for j in range(4):
        if sum(square[i][j] for i in range(4)) != MAGIC_SUM:
            return False
    if sum(square[i][i] for i in range(4)) != MAGIC_SUM:
        return False
    if sum(square[i][3 - i] for i in range(4)) != MAGIC_SUM:
        return False
    return True


@lru_cache(maxsize=1)
def generate_order4_normal_magic_squares() -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Generate all 7040 normal 4x4 magic squares."""
    squares: list[tuple[tuple[int, ...], ...]] = []
    for r0, m0 in row_candidates():
        for r1, m1 in rows_disjoint_from(m0):
            used01 = m0 | m1
            key = (
                FULL_MASK ^ used01,
                tuple(MAGIC_SUM - (r0[j] + r1[j]) for j in range(4)),
                MAGIC_SUM - (r0[0] + r1[1]),
                MAGIC_SUM - (r0[3] + r1[2]),
            )
            for r2, r3 in lower_pair_map().get(key, ()):
                square = (r0, r1, r2, r3)
                if is_magic(square):
                    squares.append(square)
    return tuple(sorted(set(squares)))


def transform_square(square: tuple[tuple[int, ...], ...], transform_id: int) -> tuple[tuple[int, ...], ...]:
    def val(i: int, j: int) -> int:
        return square[i][j]

    if transform_id == 0:
        return tuple(tuple(val(i, j) for j in range(4)) for i in range(4))
    if transform_id == 1:
        return tuple(tuple(val(3 - j, i) for j in range(4)) for i in range(4))
    if transform_id == 2:
        return tuple(tuple(val(3 - i, 3 - j) for j in range(4)) for i in range(4))
    if transform_id == 3:
        return tuple(tuple(val(j, 3 - i) for j in range(4)) for i in range(4))
    if transform_id == 4:
        return tuple(tuple(val(3 - i, j) for j in range(4)) for i in range(4))
    if transform_id == 5:
        return tuple(tuple(val(i, 3 - j) for j in range(4)) for i in range(4))
    if transform_id == 6:
        return tuple(tuple(val(j, i) for j in range(4)) for i in range(4))
    if transform_id == 7:
        return tuple(tuple(val(3 - j, 3 - i) for j in range(4)) for i in range(4))
    raise ValueError(f"bad transform id {transform_id}")


def symmetry_orbit(square: tuple[tuple[int, ...], ...]) -> tuple[tuple[tuple[int, ...], ...], ...]:
    return tuple(transform_square(square, k) for k in range(8))


def canonical_square(square: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return min(symmetry_orbit(square), key=matrix_to_flat)


@lru_cache(maxsize=1)
def essential_order4_representatives() -> tuple[tuple[tuple[int, ...], ...], ...]:
    reps = {canonical_square(square) for square in generate_order4_normal_magic_squares()}
    return tuple(sorted(reps, key=matrix_to_flat))


def admissible_one_incidence_perms() -> tuple[tuple[int, int, int, int], ...]:
    out = []
    for p in itertools.permutations(range(4)):
        main = sum(1 for i, j in enumerate(p) if i == j)
        anti = sum(1 for i, j in enumerate(p) if i + j == 3)
        if main == 1 and anti == 1:
            out.append(p)
    return tuple(sorted(out))


def perm_string(p: tuple[int, ...]) -> str:
    return "".join(str(x) for x in p)


def endpoint_for_mask(square: tuple[tuple[int, ...], ...], p: tuple[int, ...]) -> dict:
    values = [square[i][p[i]] for i in range(4)]
    t_max = min(v - 1 for v in values)
    return {
        "perm": perm_string(p),
        "values": values,
        "t_max": t_max,
        "terminal_sum": MAGIC_SUM - t_max,
    }


def endpoint_spectrum_for_squares(squares: tuple[tuple[tuple[int, ...], ...], ...]) -> dict:
    perms = admissible_one_incidence_perms()
    perm_names = [perm_string(p) for p in perms]
    terminal_counts: Counter[int] = Counter()
    mask_counts: Counter[str] = Counter()
    squares_with_24 = 0
    pairs_terminal_24 = []

    for idx, square in enumerate(squares):
        has_24 = False
        for p in perms:
            endpoint = endpoint_for_mask(square, p)
            terminal_sum = endpoint["terminal_sum"]
            terminal_counts[terminal_sum] += 1
            if terminal_sum == 24:
                has_24 = True
                mask_counts[endpoint["perm"]] += 1
                pairs_terminal_24.append(
                    {
                        "square_index": idx,
                        "perm": endpoint["perm"],
                        "values": endpoint["values"],
                    }
                )
        if has_24:
            squares_with_24 += 1

    return {
        "square_count": len(squares),
        "admissible_mask_count": len(perms),
        "pair_count": len(squares) * len(perms),
        "terminal_sum_counts": {str(k): terminal_counts[k] for k in sorted(terminal_counts)},
        "terminal_24_pair_count": len(pairs_terminal_24),
        "terminal_24_square_count": squares_with_24,
        "terminal_24_mask_counts": {k: mask_counts[k] for k in perm_names},
        "terminal_24_pairs": pairs_terminal_24,
    }


def digest_squares(squares: tuple[tuple[tuple[int, ...], ...], ...]) -> str:
    payload = json.dumps([matrix_to_lists(s) for s in squares], separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_dataset() -> dict:
    raw = generate_order4_normal_magic_squares()
    essential = essential_order4_representatives()
    return {
        "metadata": {
            "project": "Magic 24",
            "dataset": "order4_normal_magic_squares_internal",
            "generator": "scripts/enumerate_order4_endpoints.py",
            "normalization": "lexicographically minimal representative under the 8 D4 square symmetries",
            "values": "1..16",
            "magic_sum": MAGIC_SUM,
            "external_dataset_used": False,
        },
        "raw_count": len(raw),
        "essential_count": len(essential),
        "raw_sha256": digest_squares(raw),
        "essential_sha256": digest_squares(essential),
        "essential_representatives": [matrix_to_lists(s) for s in essential],
    }


def build_endpoint_results() -> dict:
    raw = generate_order4_normal_magic_squares()
    essential = essential_order4_representatives()
    return {
        "metadata": {
            "project": "Magic 24",
            "description": "Endpoint spectrum over admissible one-incidence masks for internal order-4 normal magic-square dataset.",
            "admissible_masks": [perm_string(p) for p in admissible_one_incidence_perms()],
        },
        "raw_7040": endpoint_spectrum_for_squares(raw),
        "essential_880": endpoint_spectrum_for_squares(essential),
    }


def write_outputs(root: Path) -> None:
    data_path = root / "data" / "order4_normal_essential_880.json"
    result_path = root / "results" / "order4_endpoint_spectrum.json"
    data_path.write_text(json.dumps(build_dataset(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result_path.write_text(json.dumps(build_endpoint_results(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(data_path)
    print(result_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write dataset and endpoint JSON files")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    if args.write:
        write_outputs(root)
    else:
        endpoint = dict(build_endpoint_results()["essential_880"])
        pairs = endpoint["terminal_24_pairs"]
        endpoint["terminal_24_pairs_sample"] = pairs[:5]
        endpoint["terminal_24_pairs"] = f"{len(pairs)} pairs omitted; run with --write for full JSON"
        summary = {
            "raw_count": len(generate_order4_normal_magic_squares()),
            "essential_count": len(essential_order4_representatives()),
            "endpoint_essential": endpoint,
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
