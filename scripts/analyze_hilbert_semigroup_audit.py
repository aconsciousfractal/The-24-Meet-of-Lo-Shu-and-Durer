"""Hilbert-style semigroup audit for nonnegative diagonal-magic squares.

This script is deliberately scoped.  It enumerates nonnegative integer
`4 x 4` diagonal-magic squares for small magic sums, extracts indecomposable
atoms in that finite range, and tests atom decompositions of the Magic 24
source/terminal objects and all 236 terminal-24 endpoints.

It is not a proof of the complete Hilbert basis of the cone.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import enumerate_order4_endpoints as order4


Vector = tuple[int, ...]
ATOM_CHECK_MAX_SUM = 8
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


@lru_cache(maxsize=None)
def row_compositions(total: int) -> tuple[tuple[int, int, int, int], ...]:
    rows = []
    for a in range(total + 1):
        for b in range(total - a + 1):
            for c in range(total - a - b + 1):
                d = total - a - b - c
                rows.append((a, b, c, d))
    return tuple(rows)


@lru_cache(maxsize=None)
def nonnegative_magic_squares(magic_sum: int) -> tuple[Vector, ...]:
    """Enumerate nonnegative diagonal-magic 4x4 squares with fixed sum."""

    rows = row_compositions(magic_sum)
    lower_pairs: dict[tuple[tuple[int, int, int, int], int, int], list[tuple[tuple[int, ...], tuple[int, ...]]]] = defaultdict(list)
    for r2 in rows:
        for r3 in rows:
            key = (
                tuple(r2[j] + r3[j] for j in range(4)),
                r2[2] + r3[3],
                r2[1] + r3[0],
            )
            lower_pairs[key].append((r2, r3))

    out = []
    for r0 in rows:
        for r1 in rows:
            need = (
                tuple(magic_sum - (r0[j] + r1[j]) for j in range(4)),
                magic_sum - (r0[0] + r1[1]),
                magic_sum - (r0[3] + r1[2]),
            )
            if any(value < 0 for value in need[0]) or need[1] < 0 or need[2] < 0:
                continue
            for r2, r3 in lower_pairs.get(need, []):
                out.append(tuple(r0 + r1 + r2 + r3))
    return tuple(sorted(out))


def is_decomposable(square: Vector, square_by_sum: dict[int, set[Vector]], magic_sum: int) -> bool:
    for left_sum in range(1, magic_sum):
        right_sum = magic_sum - left_sum
        for left in square_by_sum[left_sum]:
            right = tuple(square[index] - left[index] for index in range(16))
            if min(right) >= 0 and right in square_by_sum[right_sum]:
                return True
    return False


@lru_cache(maxsize=1)
def atom_audit() -> dict:
    square_by_sum: dict[int, set[Vector]] = {0: {(0,) * 16}}
    atoms_by_sum: dict[int, list[Vector]] = {}
    square_counts = {}
    atom_counts = {}
    support_counts_by_sum = {}

    for magic_sum in range(1, ATOM_CHECK_MAX_SUM + 1):
        squares = set(nonnegative_magic_squares(magic_sum))
        square_by_sum[magic_sum] = squares
        atoms = [
            square
            for square in sorted(squares)
            if not is_decomposable(square, square_by_sum, magic_sum)
        ]
        atoms_by_sum[magic_sum] = atoms
        square_counts[str(magic_sum)] = len(squares)
        atom_counts[str(magic_sum)] = len(atoms)
        support_counts_by_sum[str(magic_sum)] = counter_json(
            Counter(sum(1 for value in atom if value) for atom in atoms)
        )

    atoms = []
    for magic_sum in sorted(atoms_by_sum):
        for atom in atoms_by_sum[magic_sum]:
            atoms.append({"magic_sum": magic_sum, "flat": atom})

    return {
        "square_counts": square_counts,
        "atom_counts": atom_counts,
        "support_counts_by_sum": support_counts_by_sum,
        "atoms": atoms,
    }


def atom_matrix(atoms: list[dict]) -> np.ndarray:
    return np.array([atom["flat"] for atom in atoms], dtype=float).T


def solve_min_atom_decomposition(target: Vector, atoms: list[dict]) -> dict:
    matrix = atom_matrix(atoms)
    result = milp(
        c=np.ones(len(atoms)),
        integrality=np.ones(len(atoms)),
        bounds=Bounds(np.zeros(len(atoms)), np.full(len(atoms), np.inf)),
        constraints=LinearConstraint(matrix, np.array(target, dtype=float), np.array(target, dtype=float)),
        options={"time_limit": 30},
    )
    if not result.success:
        return {"success": False, "message": str(result.message)}
    coeffs = np.rint(result.x).astype(int)
    reconstruction = tuple(
        int(sum(coeffs[index] * atoms[index]["flat"][cell] for index in range(len(atoms))))
        for cell in range(16)
    )
    degree_counts = Counter()
    support = 0
    coeff_records = []
    for index, coeff in enumerate(coeffs):
        if coeff <= 0:
            continue
        support += 1
        degree_counts[atoms[index]["magic_sum"]] += int(coeff)
        coeff_records.append(
            {
                "atom_index": index,
                "atom_magic_sum": atoms[index]["magic_sum"],
                "coefficient": int(coeff),
            }
        )
    return {
        "success": True,
        "min_atom_count": int(coeffs.sum()),
        "support_size": support,
        "atom_magic_sum_coefficient_counts": counter_json(degree_counts),
        "coefficients": coeff_records,
        "reconstruction_matches": reconstruction == target,
    }


def magic_sum(flat: Vector) -> int:
    return sum(flat[:4])


def class_for_inside_record(record: dict) -> str:
    if record["is_exact_canonical_v4"]:
        return "exact_v4"
    if record["terminal_signature_key"] == MAIN_TERMINAL_KEY:
        return "main_extra"
    return "outside_main"


def terminal_flat(square: tuple[tuple[int, ...], ...], mask_text: str, t: int) -> Vector:
    mask = tuple(int(char) for char in mask_text)
    return tuple(
        square[i][j] - (t if mask[i] == j else 0)
        for i in range(4)
        for j in range(4)
    )


@lru_cache(maxsize=1)
def build_hilbert_semigroup_audit() -> dict:
    root = Path(__file__).resolve().parents[1]
    atoms_result = atom_audit()
    atoms = atoms_result["atoms"]
    terminal24 = load_json(root / "results" / "order4_terminal24_fingerprints.json")
    inside_out = load_json(root / "results" / "order4_inside_out_profiles.json")
    inside_by_pair = {
        (record["square_index"], record["mask"]): record
        for record in inside_out["records"]  # type: ignore[index]
    }
    squares = order4.essential_order4_representatives()

    durer_source = (
        1, 14, 15, 4,
        12, 7, 6, 9,
        8, 11, 10, 5,
        13, 2, 3, 16,
    )
    sagrada_mask = "2013"
    sagrada_perm = tuple(int(char) for char in sagrada_mask)
    durer_terminal = tuple(
        durer_source[4 * i + j] - (10 if sagrada_perm[i] == j else 0)
        for i in range(4)
        for j in range(4)
    )

    named_targets = {
        "durer_source_D": durer_source,
        "durer_terminal_D10": durer_terminal,
    }
    named_decompositions = {
        name: {
            "magic_sum": magic_sum(target),
            "decomposition": solve_min_atom_decomposition(target, atoms),
        }
        for name, target in named_targets.items()
    }

    endpoint_records = []
    min_atom_distribution = Counter()
    class_min_atom_distribution: dict[str, Counter] = defaultdict(Counter)
    degree_profile_distribution = Counter()
    failed = 0

    for record in terminal24["records"]:  # type: ignore[index]
        square = squares[record["square_index"]]
        target = terminal_flat(square, record["mask"], record["t_max"])
        inside_record = inside_by_pair[(record["square_index"], record["mask"])]
        class_name = class_for_inside_record(inside_record)
        decomposition = solve_min_atom_decomposition(target, atoms)
        if not decomposition["success"]:
            failed += 1
            continue
        min_atom_distribution[decomposition["min_atom_count"]] += 1
        class_min_atom_distribution[class_name][decomposition["min_atom_count"]] += 1
        degree_profile_distribution[
            tuple(decomposition["atom_magic_sum_coefficient_counts"].items())
        ] += 1
        endpoint_records.append(
            {
                "square_index": record["square_index"],
                "mask": record["mask"],
                "class": class_name,
                "terminal_quaterne_count": record["quaternes"]["terminal_count"],
                "decomposition": decomposition,
            }
        )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase H Hilbert-style semigroup audit",
            "description": "Finite atom audit for nonnegative diagonal-magic 4x4 squares and atom decompositions of Magic 24 targets.",
            "guardrail": "This verifies atoms only up to magic sum 8 and decompositions in the generated atom set; it is not a proof of the complete Hilbert basis.",
        },
        "atom_check_max_sum": ATOM_CHECK_MAX_SUM,
        "square_counts_by_sum": atoms_result["square_counts"],
        "atom_counts_by_sum": atoms_result["atom_counts"],
        "atom_support_counts_by_sum": atoms_result["support_counts_by_sum"],
        "atom_count_total": len(atoms),
        "atom_magic_sum_distribution": counter_json(Counter(atom["magic_sum"] for atom in atoms)),
        "named_decompositions": named_decompositions,
        "terminal24_decomposition_summary": {
            "pair_count": len(endpoint_records),
            "failed_decomposition_count": failed,
            "min_atom_count_distribution": counter_json(min_atom_distribution),
            "class_min_atom_count_distributions": {
                class_name: counter_json(counter)
                for class_name, counter in sorted(class_min_atom_distribution.items())
            },
            "degree_profile_distribution": counter_json(degree_profile_distribution),
        },
        "terminal24_records": endpoint_records,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Hilbert-Style Semigroup Audit",
        "",
        "Status: Phase H finite atom/decomposition audit",
        "",
        "## Scope",
        "",
        "This is not a complete Hilbert-basis theorem.  It enumerates",
        f"nonnegative diagonal-magic squares up to magic sum `{result['atom_check_max_sum']}`,",
        "extracts indecomposable atoms in that range, and tests decompositions",
        "of the Magic 24 targets in the generated atom set.",
        "",
        "## Atom Census",
        "",
        f"- square counts by sum: `{result['square_counts_by_sum']}`",
        f"- atom counts by sum: `{result['atom_counts_by_sum']}`",
        f"- atom support counts by sum: `{result['atom_support_counts_by_sum']}`",
        f"- total checked atoms: `{result['atom_count_total']}`",
        f"- atom magic-sum distribution: `{result['atom_magic_sum_distribution']}`",
        "",
        "## Named Decompositions",
        "",
    ]
    for name, row in result["named_decompositions"].items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- magic sum: `{row['magic_sum']}`")
        lines.append(f"- decomposition: `{row['decomposition']}`")
        lines.append("")
    summary = result["terminal24_decomposition_summary"]
    lines.extend(
        [
            "## Terminal-24 Endpoint Decompositions",
            "",
            f"- pair count: `{summary['pair_count']}`",
            f"- failed decompositions: `{summary['failed_decomposition_count']}`",
            f"- min atom-count distribution: `{summary['min_atom_count_distribution']}`",
            f"- class min atom-count distributions: `{summary['class_min_atom_count_distributions']}`",
            f"- degree-profile distribution: `{summary['degree_profile_distribution']}`",
            "",
            "## Guardrail",
            "",
            "The audit shows that the tested targets decompose in the finite atom",
            "set found through sum 8.  It does not prove that no higher-degree",
            "Hilbert-basis atoms exist in the full cone.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_hilbert_semigroup_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "hilbert_semigroup_audit.json"
        report_path = root / "results" / "HILBERT_SEMIGROUP_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "atom_count_total": result["atom_count_total"],
            "atom_counts_by_sum": result["atom_counts_by_sum"],
            "named_decompositions": result["named_decompositions"],
            "terminal24_decomposition_summary": result["terminal24_decomposition_summary"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
