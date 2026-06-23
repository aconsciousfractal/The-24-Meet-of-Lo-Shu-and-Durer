"""Parity-plane mechanism certificate for the Shu-Durer 24 bridge.

This script records the small finite residual check behind the public
"parity-plane mechanism" section.  It deliberately does not claim a
case-free symbolic proof.  The six values v in {2,4,6,8,12,14} are the nonzero residual cases supplied by the normalized parity-plane reduction; this script checks those cases rather than deriving that reduction.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUAL_VALUES = (2, 4, 6, 8, 12, 14)


def write_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rank_f2(values: list[int]) -> int:
    basis: list[int] = []
    for value in values:
        x = value
        for pivot in basis:
            x = min(x, x ^ pivot)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return len(basis)


def critical_bit(v: int) -> int:
    """Critical bit for the public six-value residual table."""
    n = v // 2
    bit = 0
    while n % 2 == 0:
        bit += 1
        n //= 2
    return bit


def affine_plane_sum_is_balanced(u: int, w: int) -> bool:
    """An affine four-plane has zero-based label sum 30 iff u OR w is 15."""
    return (u | w) == 15


def diag_sums_row_residual(offset: int, a: int, b: int, g: int, d: int, v: int) -> tuple[int, int]:
    main = [offset, offset ^ b ^ d ^ v, offset ^ a ^ g, offset ^ a ^ b ^ g ^ d]
    anti = [offset ^ g ^ d, offset ^ b ^ g ^ v, offset ^ a ^ d, offset ^ a ^ b]
    return sum(main), sum(anti)


def row_direction_constraints_hold(a: int, b: int, g: int, d: int, v: int) -> bool:
    return (
        (g | d) == 15
        and ((g ^ v) | (d ^ v)) == 15
        and (a | b) == 15
        and (a | (b ^ v)) == 15
    )


def toggle_bijection_sources(a: int, g: int, d: int, v: int) -> list[str]:
    sources = []
    if v == a:
        sources.append("a")
    if v == (g ^ d):
        sources.append("g^d")
    if v == (a ^ g ^ d):
        sources.append("a^g^d")
    return sources


def row_survivors(v: int) -> list[dict[str, Any]]:
    survivors = []
    for a, b, g, d in product(range(1, 16), repeat=4):
        if rank_f2([a, b, g, d]) != 4:
            continue
        if not row_direction_constraints_hold(a, b, g, d, v):
            continue
        sources = toggle_bijection_sources(a, g, d, v)
        if not sources:
            continue
        offsets = [offset for offset in range(16) if diag_sums_row_residual(offset, a, b, g, d, v) == (30, 30)]
        if offsets:
            survivors.append({"a": a, "b": b, "g": g, "d": d, "offsets": offsets, "sources": sources})
    return survivors


def summarize_value(v: int) -> dict[str, Any]:
    survivors = row_survivors(v)
    crit = critical_bit(v)
    a_values = sorted({row["a"] for row in survivors})
    g_values = sorted({row["g"] for row in survivors})
    nw_cover_count = sum(1 for row in survivors if affine_plane_sum_is_balanced(row["a"], row["g"]))
    return {
        "v": v,
        "critical_bit": crit,
        "direction_survivor_count": len(survivors),
        "offset_survivor_count": sum(len(row["offsets"]) for row in survivors),
        "bijection_source_values": sorted({source for row in survivors for source in row["sources"]}),
        "a_values": a_values,
        "g_values": g_values,
        "a_equals_v_for_all_survivors": a_values == [v],
        "g_has_zero_critical_bit_for_all_survivors": all(((g >> crit) & 1) == 0 for g in g_values),
        "nw_direction_covers_all_bits_count": nw_cover_count,
        "nw_bit_balance_possible": nw_cover_count > 0,
    }


def build_parity_plane_mechanism() -> dict[str, Any]:
    table = [summarize_value(v) for v in RESIDUAL_VALUES]
    return {
        "metadata": {
            "project": "The 24-Meet of Lo Shu and Durer",
            "description": "Public finite residual check for the parity-plane mechanism.",
            "scope": "Shu-Durer bridge paper; not a universal magic-square invariant.",
            "residual_values_source": "Nonzero cases supplied by the normalized parity-plane residual reduction; this script checks them rather than deriving a table-free classification.",
        },
        "definitions": {
            "nw_parity_plane_row_major_indices": [0, 2, 8, 10],
            "bit_balance_counts": [2, 2, 2, 2],
            "zero_based_balanced_sum": 30,
            "residual_values": list(RESIDUAL_VALUES),
        },
        "analytic_lemmas": {
            "affine_plane_sum": "A zero-based affine four-plane has sum 30 iff its two directions satisfy u OR w = 15.",
            "visible_b11_split": "On the NW parity plane, xor(labels)=B11, so B11 != 0 forbids bit-balance.",
        },
        "finite_residual_table": table,
        "summary": {
            "all_survivors_have_a_equals_v": all(row["a_equals_v_for_all_survivors"] for row in table),
            "all_survivors_have_g_zero_on_critical_bit": all(row["g_has_zero_critical_bit_for_all_survivors"] for row in table),
            "nw_bit_balance_possible_in_row_residual": any(row["nw_bit_balance_possible"] for row in table),
            "column_residual_by_transpose_symmetry": True,
            "proof_status": "finite_residual_check_with_six_values_not_table_free",
        },
        "guardrails": [
            "The final residual step is a six-value finite check, not a table-free symbolic proof.",
            "The residual values are scoped input cases from the normalized parity-plane reduction, not newly derived here.",
            "The mechanism is scoped to the normalized parity-plane model used in this paper.",
            "This is not a universal endpoint-24 invariant for all magic squares.",
        ],
    }


def write_report(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Parity-Plane Mechanism Report",
        "",
        "Status: public finite residual check.  The residual step is still a six-value check, not a table-free symbolic proof.",
        "",
        "## Summary",
        "",
        f"- residual values: `{data['definitions']['residual_values']}`",
        f"- all survivors have `a=v`: `{data['summary']['all_survivors_have_a_equals_v']}`",
        f"- all survivors have `g` zero on the critical bit: `{data['summary']['all_survivors_have_g_zero_on_critical_bit']}`",
        f"- NW balance possible in row residual: `{data['summary']['nw_bit_balance_possible_in_row_residual']}`",
        f"- column residual by transpose symmetry: `{data['summary']['column_residual_by_transpose_symmetry']}`",
        "",
        "## Six-Value Residual Table",
        "",
        "| v | critical bit | direction classes | offsets | a-values | g-values | NW balance possible |",
        "|---:|---:|---:|---:|---|---|---|",
    ]
    for row in data["finite_residual_table"]:
        lines.append(
            f"| {row['v']} | {row['critical_bit']} | {row['direction_survivor_count']} | "
            f"{row['offset_survivor_count']} | `{row['a_values']}` | `{row['g_values']}` | "
            f"`{row['nw_bit_balance_possible']}` |"
        )
    lines.extend(["", "## Guardrails", ""])
    lines.extend(f"- {item}" for item in data["guardrails"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write JSON and Markdown results")
    args = parser.parse_args()

    data = build_parity_plane_mechanism()
    if args.write:
        write_json(data, ROOT / "results" / "parity_plane_mechanism.json")
        write_report(data, ROOT / "results" / "PARITY_PLANE_MECHANISM_REPORT.md")
        print("wrote results/parity_plane_mechanism.json")
        print("wrote results/PARITY_PLANE_MECHANISM_REPORT.md")
    else:
        print(json.dumps(data["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()