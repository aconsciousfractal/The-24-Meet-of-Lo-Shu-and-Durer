"""APD / Prouhet-Tarry-Escott layer for the Sagrada ray.

Takemura's APD is an alternating sum of powers of permutation-diagonal sums.
Equivalently, APD_m=0 says that the even and odd permutation-diagonal
multisets have equal m-th power sums, i.e. a Prouhet-Tarry-Escott style
balance at degree m.

This script records the APD polynomials along D(t)=D-tM, first nonzero
degrees for selected t-values, and even/odd diagonal-sum multisets.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import magic24_certificates as magic24


def poly_eval(coeffs: list[int], t: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total += coeff * power
        power *= t
    return total


def even_odd_sums(t: int) -> dict[str, list[int]]:
    even = []
    odd = []
    for p in itertools.permutations(range(4)):
        value = magic24.perm_diagonal_sum(p, t)
        if magic24.perm_parity(p) == 0:
            even.append(value)
        else:
            odd.append(value)
    return {"even": sorted(even), "odd": sorted(odd)}


def power_sums(values: list[int], max_degree: int) -> dict[str, int]:
    return {str(k): sum(v**k for v in values) for k in range(1, max_degree + 1)}


def first_nonzero_degree(apd_by_degree: dict[str, list[int]], t: int) -> int | None:
    for degree in sorted(int(k) for k in apd_by_degree):
        if poly_eval(apd_by_degree[str(degree)], t) != 0:
            return degree
    return None


def build_apd_pte_analysis(max_degree: int = 8) -> dict:
    apd = {str(k): magic24.apd_polynomial(k) for k in range(1, max_degree + 1)}
    special_t = [0, 4, 10, 16]
    first_nonzero = {
        str(t): first_nonzero_degree(apd, t)
        for t in range(0, 11)
    }
    special_records = {}
    for t in special_t:
        parity_sums = even_odd_sums(t)
        even_power_sums = power_sums(parity_sums["even"], max_degree)
        odd_power_sums = power_sums(parity_sums["odd"], max_degree)
        special_records[str(t)] = {
            "magic_sum": 34 - t,
            "inside_bounded_sagrada_interval": 0 <= t <= 10,
            "even_diagonal_sums": parity_sums["even"],
            "odd_diagonal_sums": parity_sums["odd"],
            "even_power_sums": even_power_sums,
            "odd_power_sums": odd_power_sums,
            "apd_values": {
                str(k): even_power_sums[str(k)] - odd_power_sums[str(k)]
                for k in range(1, max_degree + 1)
            },
            "first_nonzero_degree_up_to_max": first_nonzero_degree(apd, t),
        }

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase G",
            "description": "APD/PTE replay along the Durer/Sagrada ray.",
            "max_degree": max_degree,
            "pte_reading": "APD_m=0 iff even and odd permutation-diagonal sums have equal m-th power sums.",
        },
        "apd_polynomials_coefficients_ascending": apd,
        "apd_zero_polynomials": [
            str(k) for k, coeffs in apd.items() if coeffs == [0]
        ],
        "apd3_factorization": "-24*t*(t-4)*(t-16)",
        "bounded_interval_first_nonzero_degree": first_nonzero,
        "special_t_records": special_records,
        "interpretation": {
            "source_t0": "Durer has APD_1=APD_2=APD_3=0 and first nonzero degree 4 in this replay range.",
            "terminal_t10": "The bounded terminal value t=10 has first nonzero degree 3; terminality is not an APD-zero condition.",
            "internal_t4": "The internal root t=4 restores APD_3=0 but is not the bounded terminal endpoint.",
            "external_t16": "The root t=16 is outside the bounded Sagrada interval.",
        },
    }


def write_report(result: dict, path: Path) -> None:
    apd = result["apd_polynomials_coefficients_ascending"]
    first = result["bounded_interval_first_nonzero_degree"]
    special = result["special_t_records"]
    lines = [
        "# APD / PTE Report",
        "",
        "Status: Phase G initial exact replay",
        "",
        "## PTE Reading",
        "",
        "`APD_m=0` is equivalent to equality of the `m`-th power sums of",
        "the even and odd permutation-diagonal sum multisets.  Along the",
        "Sagrada ray this gives a bounded Prouhet-Tarry-Escott style",
        "deformation, not a new universal invariant of `24`.",
        "",
        "## APD Polynomials",
        "",
        f"- zero APD polynomials: `{result['apd_zero_polynomials']}`",
        f"- `APD_3(t)`: `{apd['3']}` = `-24*t*(t-4)*(t-16)`",
        f"- `APD_4(t)`: `{apd['4']}`",
        "",
        "## First Nonzero Degree On The Bounded Interval",
        "",
        "```text",
    ]
    for t in range(0, 11):
        lines.append(f"t={t:2d}, sum={34-t:2d}, m1<={result['metadata']['max_degree']}: {first[str(t)]}")
    lines.extend([
        "```",
        "",
        "## Special Values",
        "",
    ])
    for t in ("0", "4", "10", "16"):
        row = special[t]
        lines.extend(
            [
                f"### t={t}",
                "",
                f"- magic sum: `{row['magic_sum']}`",
                f"- inside bounded interval: `{row['inside_bounded_sagrada_interval']}`",
                f"- first nonzero degree up to max: `{row['first_nonzero_degree_up_to_max']}`",
                f"- APD values: `{row['apd_values']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Guardrail",
            "",
            "The PTE/APD layer explains the parity-power balance of permutation",
            "diagonals.  It does not say that `24` is the APD-symmetric point;",
            "at the bounded terminal endpoint `t=10`, `APD_3` is nonzero.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write APD/PTE JSON and report")
    parser.add_argument("--max-degree", type=int, default=8)
    args = parser.parse_args()

    result = build_apd_pte_analysis(args.max_degree)
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "apd_pte_analysis.json"
        report_path = root / "results" / "APD_PTE_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "apd_zero_polynomials": result["apd_zero_polynomials"],
            "apd3": result["apd_polynomials_coefficients_ascending"]["3"],
            "first_nonzero": result["bounded_interval_first_nonzero_degree"],
            "special_t": {
                t: result["special_t_records"][t]["first_nonzero_degree_up_to_max"]
                for t in ("0", "4", "10", "16")
            },
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
