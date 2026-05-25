"""Structural fingerprints for the order-4 terminal-24 cases.

This is the second Phase-C layer.  The dataset generator tells us that 236
essential square-mask pairs terminate at magic sum 24.  This script computes
first-pass invariants for those pairs:

- selected-value signatures;
- source and terminal permutation-diagonal sets;
- APD-style square fingerprints;
- quaterne transport decompositions.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import enumerate_order4_endpoints as order4


Cell = tuple[int, int]
Square = tuple[tuple[int, ...], ...]
Perm = tuple[int, int, int, int]


def perm_from_string(text: str) -> Perm:
    return tuple(int(c) for c in text)  # type: ignore[return-value]


def perm_string(p: Perm) -> str:
    return "".join(str(x) for x in p)


def perm_parity(p: Perm) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return inv % 2


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[q[i]] for i in range(4))  # type: ignore[return-value]


def inverse(p: Perm) -> Perm:
    out = [0] * 4
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)  # type: ignore[return-value]


def perm_order(p: Perm) -> int:
    ident = (0, 1, 2, 3)
    current = ident
    for k in range(1, 25):
        current = compose(p, current)
        if current == ident:
            return k
    raise ValueError(f"order search exceeded bound for {p!r}")


def is_subgroup(perms: set[Perm]) -> bool:
    ident = (0, 1, 2, 3)
    if ident not in perms:
        return False
    for p in perms:
        if inverse(p) not in perms:
            return False
        for q in perms:
            if compose(p, q) not in perms:
                return False
    return True


def order_profile(perms: set[Perm]) -> str:
    counts = Counter(perm_order(p) for p in perms)
    return ",".join(f"{k}:{counts[k]}" for k in sorted(counts))


def all_perms() -> tuple[Perm, ...]:
    return tuple(itertools.permutations(range(4)))  # type: ignore[return-value]


def all_cells() -> tuple[Cell, ...]:
    return tuple((i, j) for i in range(4) for j in range(4))


def diagonal_sum(square: Square, p: Perm) -> int:
    return sum(square[i][p[i]] for i in range(4))


def ray_diagonal_sum(square: Square, mask: Perm, t: int, p: Perm) -> int:
    incidence = sum(1 for i in range(4) if p[i] == mask[i])
    return diagonal_sum(square, p) - t * incidence


def source_diagonal_set(square: Square) -> tuple[str, ...]:
    return tuple(perm_string(p) for p in all_perms() if diagonal_sum(square, p) == 34)


def terminal_diagonal_set(square: Square, mask: Perm, t: int) -> tuple[str, ...]:
    target = 34 - t
    return tuple(
        perm_string(p)
        for p in all_perms()
        if ray_diagonal_sum(square, mask, t, p) == target
    )


def apd_vector(square: Square) -> tuple[int, int, int, int]:
    values = []
    for power in range(1, 5):
        total = 0
        for p in all_perms():
            term = diagonal_sum(square, p) ** power
            total += term if perm_parity(p) == 0 else -term
        values.append(total)
    return tuple(values)  # type: ignore[return-value]


def selected_values(square: Square, mask: Perm) -> tuple[int, int, int, int]:
    return tuple(square[i][mask[i]] for i in range(4))  # type: ignore[return-value]


def source_quaterne_decomposition(square: Square, mask: Perm, t: int) -> dict:
    source_h34 = Counter()
    terminal_decomp = Counter()
    terminal_count = 0
    for cells in itertools.combinations(all_cells(), 4):
        source_sum = sum(square[i][j] for i, j in cells)
        incidence = sum(1 for i, j in cells if mask[i] == j)
        if source_sum == 34:
            source_h34[incidence] += 1
        if source_sum - t * incidence == 34 - t:
            terminal_count += 1
            terminal_decomp[(source_sum, incidence)] += 1

    return {
        "source_h34_count": sum(source_h34.values()),
        "source_h34_incidence": {str(k): source_h34[k] for k in range(5)},
        "terminal_count": terminal_count,
        "terminal_decomposition": {
            f"source_{source_sum}_incidence_{incidence}": terminal_decomp[
                (source_sum, incidence)
            ]
            for source_sum, incidence in sorted(terminal_decomp)
        },
    }


def source_h34_count(square: Square) -> int:
    return sum(
        1
        for cells in itertools.combinations(all_cells(), 4)
        if sum(square[i][j] for i, j in cells) == 34
    )


def signature_counter(counter: Counter) -> dict[str, int]:
    return {str(k): counter[k] for k in sorted(counter, key=str)}


@lru_cache(maxsize=1)
def classify_pairs() -> dict:
    squares = order4.essential_order4_representatives()
    endpoint = order4.endpoint_spectrum_for_squares(squares)
    pairs = endpoint["terminal_24_pairs"]

    apd_by_square = [apd_vector(square) for square in squares]
    apd_class_counts = Counter(apd_by_square)
    all_source_h34_counts = Counter(source_h34_count(square) for square in squares)
    terminal_apd_counts = Counter()
    selected_value_counts = Counter()
    min_multiplicity_counts = Counter()
    source_diagonal_size_counts = Counter()
    terminal_diagonal_size_counts = Counter()
    terminal_diagonal_set_counts = Counter()
    terminal_subgroup_counts = Counter()
    terminal_order_profile_counts = Counter()
    source_h34_counts = Counter()
    terminal_quaterne_counts = Counter()
    terminal_decomposition_counts = Counter()

    records = []
    for pair in pairs:
        idx = pair["square_index"]
        square = squares[idx]
        mask = perm_from_string(pair["perm"])
        endpoint_row = order4.endpoint_for_mask(square, mask)
        t = endpoint_row["t_max"]
        values = selected_values(square, mask)
        sorted_values = tuple(sorted(values))
        source_diags = source_diagonal_set(square)
        terminal_diags = terminal_diagonal_set(square, mask, t)
        terminal_perm_set = {perm_from_string(p) for p in terminal_diags}
        terminal_is_subgroup = is_subgroup(terminal_perm_set)
        q = source_quaterne_decomposition(square, mask, t)
        apd = apd_by_square[idx]

        selected_value_counts[sorted_values] += 1
        min_multiplicity_counts[values.count(min(values))] += 1
        source_diagonal_size_counts[len(source_diags)] += 1
        terminal_diagonal_size_counts[len(terminal_diags)] += 1
        terminal_diagonal_set_counts[terminal_diags] += 1
        terminal_subgroup_counts[str(terminal_is_subgroup)] += 1
        if terminal_is_subgroup:
            terminal_order_profile_counts[order_profile(terminal_perm_set)] += 1
        terminal_apd_counts[apd] += 1
        source_h34_counts[q["source_h34_count"]] += 1
        terminal_quaterne_counts[q["terminal_count"]] += 1
        terminal_decomposition_counts[tuple(q["terminal_decomposition"].items())] += 1

        records.append(
            {
                "square_index": idx,
                "mask": pair["perm"],
                "values": list(values),
                "sorted_values": list(sorted_values),
                "t_max": t,
                "apd_vector": list(apd),
                "apd_global_class_size": apd_class_counts[apd],
                "source_diagonal_set": list(source_diags),
                "terminal_diagonal_set": list(terminal_diags),
                "terminal_diagonal_is_subgroup": terminal_is_subgroup,
                "terminal_diagonal_order_profile": (
                    order_profile(terminal_perm_set) if terminal_is_subgroup else None
                ),
                "quaternes": q,
            }
        )

    top_terminal_sets = [
        {
            "terminal_diagonal_set": list(diags),
            "count": count,
            "is_subgroup": is_subgroup({perm_from_string(p) for p in diags}),
        }
        for diags, count in terminal_diagonal_set_counts.most_common(12)
    ]

    return {
        "metadata": {
            "project": "Magic 24",
            "description": "First structural fingerprint pass for the 236 essential terminal-24 order-4 pairs.",
            "source_dataset": "data/order4_normal_essential_880.json",
            "source_endpoint_spectrum": "results/order4_endpoint_spectrum.json",
        },
        "pair_count": len(records),
        "square_count": len({r["square_index"] for r in records}),
        "apd_square_class_count": len(apd_class_counts),
        "terminal_24_apd_class_count": len(terminal_apd_counts),
        "singleton_apd_terminal_pair_count": sum(
            count for apd, count in terminal_apd_counts.items() if apd_class_counts[apd] == 1
        ),
        "all_square_source_h34_count_distribution": signature_counter(all_source_h34_counts),
        "selected_value_signature_counts": signature_counter(selected_value_counts),
        "min_multiplicity_counts": signature_counter(min_multiplicity_counts),
        "source_diagonal_size_counts": signature_counter(source_diagonal_size_counts),
        "terminal_diagonal_size_counts": signature_counter(terminal_diagonal_size_counts),
        "terminal_diagonal_subgroup_counts": signature_counter(terminal_subgroup_counts),
        "terminal_diagonal_order_profile_counts": signature_counter(
            terminal_order_profile_counts
        ),
        "source_h34_count_distribution": signature_counter(source_h34_counts),
        "terminal_quaterne_count_distribution": signature_counter(terminal_quaterne_counts),
        "terminal_decomposition_type_count": len(terminal_decomposition_counts),
        "top_terminal_diagonal_sets": top_terminal_sets,
        "records": records,
    }


def write_outputs(root: Path) -> None:
    result = classify_pairs()
    path = root / "results" / "order4_terminal24_fingerprints.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write terminal-24 fingerprint JSON")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    result = classify_pairs()
    if args.write:
        path = root / "results" / "order4_terminal24_fingerprints.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = dict(result)
        summary["records_sample"] = summary["records"][:3]
        summary["records"] = f"{len(result['records'])} records omitted; run with --write for full JSON"
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
