"""APD/PTE profiles across all Phase-C one-incidence rays.

The initial Phase-G APD/PTE replay was local to the Durer/Sagrada ray.  This
script extends the same invariant to all 880 essential order-4 normal magic
squares and their 8 admissible one-incidence masks.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import analyze_order4_terminal24 as terminal24
import enumerate_order4_endpoints as order4


Square = tuple[tuple[int, ...], ...]
Perm = tuple[int, int, int, int]


def poly_add(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for idx in range(size):
        out[idx] = (left[idx] if idx < len(left) else 0) + (
            right[idx] if idx < len(right) else 0
        )
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def signed_linear_power(base: int, incidence: int, degree: int, sign: int) -> list[int]:
    coeffs = []
    for k in range(degree + 1):
        coeff = math.comb(degree, k) * (base ** (degree - k)) * ((-incidence) ** k)
        coeffs.append(sign * coeff)
    return coeffs


def poly_eval(coeffs: list[int], t: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total += coeff * power
        power *= t
    return total


def poly_is_zero(coeffs: list[int]) -> bool:
    return all(coeff == 0 for coeff in coeffs)


def diagonal_sum(square: Square, perm: Perm) -> int:
    return sum(square[i][perm[i]] for i in range(4))


def mask_incidence(mask: Perm, perm: Perm) -> int:
    return sum(1 for i in range(4) if perm[i] == mask[i])


def apd_polynomials_for_ray(square: Square, mask: Perm, max_degree: int) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for degree in range(1, max_degree + 1):
        coeffs = [0]
        for perm in terminal24.all_perms():
            sign = 1 if terminal24.perm_parity(perm) == 0 else -1
            coeffs = poly_add(
                coeffs,
                signed_linear_power(
                    diagonal_sum(square, perm),
                    mask_incidence(mask, perm),
                    degree,
                    sign,
                ),
            )
        out[str(degree)] = coeffs
    return out


def first_nonzero_polynomial_degree(polynomials: dict[str, list[int]]) -> int | None:
    for degree in sorted(int(key) for key in polynomials):
        if not poly_is_zero(polynomials[str(degree)]):
            return degree
    return None


def first_nonzero_value_degree(polynomials: dict[str, list[int]], t: int) -> int | None:
    for degree in sorted(int(key) for key in polynomials):
        if poly_eval(polynomials[str(degree)], t) != 0:
            return degree
    return None


def key(value: object) -> str:
    return "none" if value is None else str(value)


def counter_json(counter: Counter) -> dict[str, int]:
    return {key(k): counter[k] for k in sorted(counter, key=lambda item: (str(type(item)), str(item)))}


def nested_counter_json(counter: Counter[tuple[object, object]]) -> dict[str, dict[str, int]]:
    grouped: dict[str, dict[str, int]] = defaultdict(dict)
    for (left, right), count in sorted(counter.items(), key=lambda item: (str(item[0][0]), str(item[0][1]))):
        grouped[key(left)][key(right)] = count
    return dict(grouped)


def build_order4_apd_pte_profiles(max_degree: int = 8) -> dict:
    squares = order4.essential_order4_representatives()
    masks = order4.admissible_one_incidence_perms()

    endpoint_counts = Counter()
    polynomial_m1_counts = Counter()
    terminal_m1_counts = Counter()
    source_m1_counts = Counter()
    endpoint_terminal_m1_counts = Counter()
    endpoint_polynomial_m1_counts = Counter()
    endpoint_source_m1_counts = Counter()
    endpoint_apd3_terminal_zero_counts = Counter()
    endpoint_all_zero_terminal_counts = Counter()
    terminal24_records = []
    sample_records = []
    canonical_durer_sagrada = None

    for square_index, square in enumerate(squares):
        for mask in masks:
            mask_text = order4.perm_string(mask)
            endpoint = order4.endpoint_for_mask(square, mask)
            t_max = endpoint["t_max"]
            terminal_sum = endpoint["terminal_sum"]
            polynomials = apd_polynomials_for_ray(square, mask, max_degree)
            polynomial_m1 = first_nonzero_polynomial_degree(polynomials)
            source_m1 = first_nonzero_value_degree(polynomials, 0)
            terminal_m1 = first_nonzero_value_degree(polynomials, t_max)
            terminal_apd_values = {
                str(degree): poly_eval(polynomials[str(degree)], t_max)
                for degree in range(1, max_degree + 1)
            }
            apd3_terminal_zero = terminal_apd_values.get("3") == 0
            all_zero_terminal = terminal_m1 is None

            endpoint_counts[terminal_sum] += 1
            polynomial_m1_counts[polynomial_m1] += 1
            source_m1_counts[source_m1] += 1
            terminal_m1_counts[terminal_m1] += 1
            endpoint_terminal_m1_counts[(terminal_sum, terminal_m1)] += 1
            endpoint_polynomial_m1_counts[(terminal_sum, polynomial_m1)] += 1
            endpoint_source_m1_counts[(terminal_sum, source_m1)] += 1
            endpoint_apd3_terminal_zero_counts[(terminal_sum, apd3_terminal_zero)] += 1
            endpoint_all_zero_terminal_counts[(terminal_sum, all_zero_terminal)] += 1

            record = {
                "square_index": square_index,
                "mask": mask_text,
                "endpoint": terminal_sum,
                "t_max": t_max,
                "polynomial_first_nonzero_degree": polynomial_m1,
                "source_first_nonzero_degree": source_m1,
                "terminal_first_nonzero_degree": terminal_m1,
                "terminal_apd3_zero": apd3_terminal_zero,
                "terminal_apd_values": terminal_apd_values,
                "apd3_polynomial_coefficients": polynomials["3"],
            }
            if len(sample_records) < 12:
                sample_records.append(record)
            if terminal_sum == 24:
                terminal24_records.append(record)
            if square_index == 174 and mask_text == "1203":
                canonical_durer_sagrada = record

    endpoint_summary = {}
    for endpoint in sorted(endpoint_counts):
        endpoint_summary[str(endpoint)] = {
            "pair_count": endpoint_counts[endpoint],
            "terminal_first_nonzero_degree_counts": {
                key(m1): endpoint_terminal_m1_counts[(endpoint, m1)]
                for m1 in sorted(
                    {m1 for e, m1 in endpoint_terminal_m1_counts if e == endpoint},
                    key=lambda item: (item is None, item if item is not None else 999),
                )
            },
            "source_first_nonzero_degree_counts": {
                key(m1): endpoint_source_m1_counts[(endpoint, m1)]
                for m1 in sorted(
                    {m1 for e, m1 in endpoint_source_m1_counts if e == endpoint},
                    key=lambda item: (item is None, item if item is not None else 999),
                )
            },
            "polynomial_first_nonzero_degree_counts": {
                key(m1): endpoint_polynomial_m1_counts[(endpoint, m1)]
                for m1 in sorted(
                    {m1 for e, m1 in endpoint_polynomial_m1_counts if e == endpoint},
                    key=lambda item: (item is None, item if item is not None else 999),
                )
            },
            "terminal_apd3_zero_counts": {
                str(flag): endpoint_apd3_terminal_zero_counts[(endpoint, flag)]
                for flag in (False, True)
                if (endpoint, flag) in endpoint_apd3_terminal_zero_counts
            },
            "terminal_all_zero_up_to_max_counts": {
                str(flag): endpoint_all_zero_terminal_counts[(endpoint, flag)]
                for flag in (False, True)
                if (endpoint, flag) in endpoint_all_zero_terminal_counts
            },
        }

    terminal24_terminal_m1 = Counter(row["terminal_first_nonzero_degree"] for row in terminal24_records)
    terminal24_polynomial_m1 = Counter(row["polynomial_first_nonzero_degree"] for row in terminal24_records)
    terminal24_apd3_zero = Counter(row["terminal_apd3_zero"] for row in terminal24_records)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase G APD/PTE extension",
            "description": "APD/PTE first-appearance profiles across all 7040 essential order-4 one-incidence rays.",
            "max_degree": max_degree,
            "pair_count": len(squares) * len(masks),
            "square_count": len(squares),
            "mask_count": len(masks),
        },
        "global_counts": {
            "endpoint_counts": counter_json(endpoint_counts),
            "polynomial_first_nonzero_degree_counts": counter_json(polynomial_m1_counts),
            "source_first_nonzero_degree_counts": counter_json(source_m1_counts),
            "terminal_first_nonzero_degree_counts": counter_json(terminal_m1_counts),
            "endpoint_terminal_first_nonzero_degree_counts": nested_counter_json(
                endpoint_terminal_m1_counts
            ),
            "endpoint_polynomial_first_nonzero_degree_counts": nested_counter_json(
                endpoint_polynomial_m1_counts
            ),
        },
        "endpoint_summary": endpoint_summary,
        "terminal24_summary": {
            "pair_count": len(terminal24_records),
            "terminal_first_nonzero_degree_counts": counter_json(terminal24_terminal_m1),
            "polynomial_first_nonzero_degree_counts": counter_json(terminal24_polynomial_m1),
            "terminal_apd3_zero_counts": counter_json(terminal24_apd3_zero),
        },
        "canonical_durer_sagrada_record": canonical_durer_sagrada,
        "sample_records": sample_records,
        "interpretation": {
            "terminal24_not_isolated_by_apd_m1": (
                "Endpoint 24 is compared against all endpoints by first nonzero "
                "APD degree at the bounded terminal value."
            ),
            "terminal_apd3_zero_guardrail": (
                "A terminal APD3 zero is tracked separately because the local "
                "Durer/Sagrada terminal has APD3 nonzero."
            ),
        },
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Order-4 APD/PTE Profile Report",
        "",
        "Status: Phase G APD/PTE extension across Phase-C rays",
        "",
        "## Global Counts",
        "",
        f"- pairs: `{result['metadata']['pair_count']}`",
        f"- max APD degree checked: `{result['metadata']['max_degree']}`",
        f"- endpoint counts: `{result['global_counts']['endpoint_counts']}`",
        f"- terminal first-nonzero degree counts: `{result['global_counts']['terminal_first_nonzero_degree_counts']}`",
        f"- polynomial first-nonzero degree counts: `{result['global_counts']['polynomial_first_nonzero_degree_counts']}`",
        "",
        "## Endpoint 24",
        "",
        f"- pair count: `{result['terminal24_summary']['pair_count']}`",
        f"- terminal first-nonzero degree counts: `{result['terminal24_summary']['terminal_first_nonzero_degree_counts']}`",
        f"- polynomial first-nonzero degree counts: `{result['terminal24_summary']['polynomial_first_nonzero_degree_counts']}`",
        f"- terminal APD3 zero counts: `{result['terminal24_summary']['terminal_apd3_zero_counts']}`",
        "",
        "## Canonical Durer/Sagrada Record",
        "",
        "```json",
        json.dumps(result["canonical_durer_sagrada_record"], indent=2, sort_keys=True),
        "```",
        "",
        "## Endpoint Summary",
        "",
        "```text",
    ]
    for endpoint, summary in result["endpoint_summary"].items():
        lines.append(
            f"{endpoint}: pairs={summary['pair_count']}, "
            f"terminal_m1={summary['terminal_first_nonzero_degree_counts']}, "
            f"APD3_zero={summary['terminal_apd3_zero_counts']}"
        )
    lines.extend(
        [
            "```",
            "",
            "## Guardrail",
            "",
            "This is an APD/PTE stratification, not an endpoint theorem by itself.",
            "Endpoint `24` should only be claimed APD-special if the endpoint",
            "summary separates it from the other terminal sums.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--max-degree", type=int, default=8)
    args = parser.parse_args()

    result = build_order4_apd_pte_profiles(args.max_degree)
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "order4_apd_pte_profiles.json"
        report_path = root / "results" / "ORDER4_APD_PTE_PROFILE_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "global_terminal_m1": result["global_counts"]["terminal_first_nonzero_degree_counts"],
            "terminal24": result["terminal24_summary"],
            "canonical_durer_sagrada_record": result["canonical_durer_sagrada_record"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
