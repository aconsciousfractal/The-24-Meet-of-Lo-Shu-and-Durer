"""Morse-Hedlund/Prouhet family-fit test for Durer/Sagrada.

Sergeyev's paper displays a six-parameter 4x4 magic-square family with
constraint a+b=c+d.  This script tests whether the Durer/Sagrada source,
terminal point, and full Sagrada direction fit that family under transpose,
row/column relabeling, and value complement.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

import magic24_certificates as magic24


Square = tuple[tuple[int, int, int, int], ...]
Perm = tuple[int, int, int, int]


def morse_hedlund_square(a: int, b: int, c: int, d: int, k1: int, k2: int) -> Square:
    return (
        (d + k1 + k2, a, b, c + k1 + k2),
        (c + k1, b + k2, a + k2, d + k1),
        (c + k2, b + k1, a + k1, d + k2),
        (d, a + k1 + k2, b + k1 + k2, c),
    )


def family_parameters(square: Square) -> dict | None:
    a = square[0][1]
    b = square[0][2]
    c = square[3][3]
    d = square[3][0]
    k1 = square[2][2] - a
    k2 = square[1][1] - b
    if a + b != c + d:
        return None
    expected = morse_hedlund_square(a, b, c, d, k1, k2)
    if expected != square:
        return None
    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "k1": k1,
        "k2": k2,
        "magic_sum": 2 * (a + b + k1 + k2),
    }


def in_family(square: Square) -> bool:
    return family_parameters(square) is not None


def complement(square: Square) -> Square:
    return tuple(tuple(17 - value for value in row) for row in square)  # type: ignore[return-value]


def transpose(square: Square) -> Square:
    return tuple(tuple(square[j][i] for j in range(4)) for i in range(4))  # type: ignore[return-value]


def row_col_permute(square: Square, row_perm: Perm, col_perm: Perm) -> Square:
    return tuple(
        tuple(square[row_perm[i]][col_perm[j]] for j in range(4))
        for i in range(4)
    )  # type: ignore[return-value]


def transform_square(
    square: Square,
    transpose_first: bool,
    row_perm: Perm,
    col_perm: Perm,
    complement_values: bool,
) -> Square:
    out = transpose(square) if transpose_first else square
    out = row_col_permute(out, row_perm, col_perm)
    return complement(out) if complement_values else out


def mask_matrix(mask: Perm, value: int = 1) -> Square:
    return tuple(
        tuple(value if mask[i] == j else 0 for j in range(4))
        for i in range(4)
    )  # type: ignore[return-value]


def transform_mask_matrix(
    mask: Perm,
    transpose_first: bool,
    row_perm: Perm,
    col_perm: Perm,
) -> Square:
    return transform_square(mask_matrix(mask), transpose_first, row_perm, col_perm, False)


def sagrada_terminal_square() -> Square:
    mask = mask_matrix(magic24.SAGRADA_MASK_PERM)
    return tuple(
        tuple(magic24.DURER_COMPLEMENT[i][j] - 10 * mask[i][j] for j in range(4))
        for i in range(4)
    )  # type: ignore[return-value]


def matrix_add(left: Square, right: Square, scale: int = 1) -> Square:
    return tuple(
        tuple(left[i][j] + scale * right[i][j] for j in range(4))
        for i in range(4)
    )  # type: ignore[return-value]


def flat(square: Square) -> tuple[int, ...]:
    return tuple(value for row in square for value in row)


def transform_records(square: Square, mask: Perm) -> Iterable[dict]:
    perms = tuple(itertools.permutations(range(4)))  # type: ignore[assignment]
    for complement_values in (False, True):
        base_square = complement(square) if complement_values else square
        direction_sign = -1 if complement_values else 1
        for transpose_first in (False, True):
            for row_perm in perms:
                for col_perm in perms:
                    transformed_source = transform_square(
                        square,
                        transpose_first,
                        row_perm,
                        col_perm,
                        complement_values,
                    )
                    transformed_terminal = transform_square(
                        sagrada_terminal_square(),
                        transpose_first,
                        row_perm,
                        col_perm,
                        complement_values,
                    )
                    transformed_mask = transform_mask_matrix(
                        mask,
                        transpose_first,
                        row_perm,
                        col_perm,
                    )
                    direction = tuple(
                        tuple(direction_sign * transformed_mask[i][j] for j in range(4))
                        for i in range(4)
                    )  # type: ignore[assignment]
                    source_params = family_parameters(transformed_source)
                    terminal_params = family_parameters(transformed_terminal)
                    direction_params = family_parameters(direction)
                    ray_fit = (
                        source_params is not None
                        and terminal_params is not None
                        and direction_params is not None
                    )
                    yield {
                        "transpose_first": transpose_first,
                        "row_perm": list(row_perm),
                        "col_perm": list(col_perm),
                        "complement_values": complement_values,
                        "source_in_family": source_params is not None,
                        "terminal_in_family": terminal_params is not None,
                        "direction_in_linear_family": direction_params is not None,
                        "ray_in_family": ray_fit,
                        "source_parameters": source_params,
                        "terminal_parameters": terminal_params,
                        "direction_parameters": direction_params,
                        "source_flat": list(flat(transformed_source)),
                        "terminal_flat": list(flat(transformed_terminal)),
                        "direction_flat": list(flat(direction)),
                    }


def identity_record() -> dict:
    square = magic24.DURER_COMPLEMENT
    mask = magic24.SAGRADA_MASK_PERM
    source = square
    terminal = sagrada_terminal_square()
    direction = tuple(tuple(-1 if mask[i] == j else 0 for j in range(4)) for i in range(4))
    return {
        "source_parameters": family_parameters(source),
        "terminal_parameters": family_parameters(terminal),
        "negative_mask_direction_parameters": family_parameters(direction),
        "source_in_family": in_family(source),
        "terminal_in_family": in_family(terminal),
        "negative_mask_direction_in_linear_family": in_family(direction),
        "ray_in_family": in_family(source) and in_family(direction),
    }


def compact_record(record: dict) -> dict:
    return {
        "transpose_first": record["transpose_first"],
        "row_perm": record["row_perm"],
        "col_perm": record["col_perm"],
        "complement_values": record["complement_values"],
        "source_parameters": record["source_parameters"],
        "terminal_parameters": record["terminal_parameters"],
        "direction_parameters": record["direction_parameters"],
    }


def build_morse_hedlund_family_fit() -> dict:
    square = magic24.DURER_COMPLEMENT
    mask = magic24.SAGRADA_MASK_PERM
    records = list(transform_records(square, mask))

    source_fits = [record for record in records if record["source_in_family"]]
    terminal_fits = [record for record in records if record["terminal_in_family"]]
    direction_fits = [record for record in records if record["direction_in_linear_family"]]
    ray_fits = [record for record in records if record["ray_in_family"]]

    source_fit_by_scope = Counter(
        (record["transpose_first"], record["complement_values"]) for record in source_fits
    )
    terminal_fit_by_scope = Counter(
        (record["transpose_first"], record["complement_values"]) for record in terminal_fits
    )
    direction_fit_by_scope = Counter(
        (record["transpose_first"], record["complement_values"]) for record in direction_fits
    )
    ray_fit_by_scope = Counter(
        (record["transpose_first"], record["complement_values"]) for record in ray_fits
    )

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase G Morse-Hedlund/Prouhet family-fit test",
            "family": (
                "[[d+k1+k2,a,b,c+k1+k2],[c+k1,b+k2,a+k2,d+k1],"
                "[c+k2,b+k1,a+k1,d+k2],[d,a+k1+k2,b+k1+k2,c]], a+b=c+d"
            ),
            "transform_scope": "transpose optional x row permutations x column permutations x value complement",
            "transform_count": len(records),
        },
        "identity_orientation": identity_record(),
        "fit_counts": {
            "source": len(source_fits),
            "terminal": len(terminal_fits),
            "direction": len(direction_fits),
            "ray": len(ray_fits),
        },
        "fit_counts_by_transpose_and_complement": {
            "source": {
                f"transpose={t},complement={c}": count
                for (t, c), count in sorted(source_fit_by_scope.items())
            },
            "terminal": {
                f"transpose={t},complement={c}": count
                for (t, c), count in sorted(terminal_fit_by_scope.items())
            },
            "direction": {
                f"transpose={t},complement={c}": count
                for (t, c), count in sorted(direction_fit_by_scope.items())
            },
            "ray": {
                f"transpose={t},complement={c}": count
                for (t, c), count in sorted(ray_fit_by_scope.items())
            },
        },
        "first_source_fit": compact_record(source_fits[0]) if source_fits else None,
        "first_terminal_fit": compact_record(terminal_fits[0]) if terminal_fits else None,
        "first_direction_fit": compact_record(direction_fits[0]) if direction_fits else None,
        "first_ray_fit": compact_record(ray_fits[0]) if ray_fits else None,
        "conclusion": {
            "source_fits_family": bool(source_fits),
            "terminal_fits_family": bool(terminal_fits),
            "direction_fits_linear_family": bool(direction_fits),
            "full_sagrada_ray_fits_family_under_tested_scope": bool(ray_fits),
        },
    }


def write_report(result: dict, path: Path) -> None:
    conclusion = result["conclusion"]
    lines = [
        "# Morse-Hedlund / Prouhet Family-Fit Report",
        "",
        "Status: Phase G family-fit test",
        "",
        "## Transform Scope",
        "",
        f"- transforms checked: `{result['metadata']['transform_count']}`",
        "- scope: optional transpose, arbitrary row permutation, arbitrary column",
        "  permutation, and optional value complement.",
        "",
        "## Identity Orientation",
        "",
        f"- source in family: `{result['identity_orientation']['source_in_family']}`",
        f"- terminal in family: `{result['identity_orientation']['terminal_in_family']}`",
        f"- negative mask direction in linear family: `{result['identity_orientation']['negative_mask_direction_in_linear_family']}`",
        f"- ray in family: `{result['identity_orientation']['ray_in_family']}`",
        f"- source parameters: `{result['identity_orientation']['source_parameters']}`",
        "",
        "## Fit Counts",
        "",
        f"- source fits: `{result['fit_counts']['source']}`",
        f"- terminal fits: `{result['fit_counts']['terminal']}`",
        f"- direction fits: `{result['fit_counts']['direction']}`",
        f"- full ray fits: `{result['fit_counts']['ray']}`",
        "",
        "## Conclusion",
        "",
        f"- source fits family: `{conclusion['source_fits_family']}`",
        f"- terminal fits family: `{conclusion['terminal_fits_family']}`",
        f"- direction fits linear family: `{conclusion['direction_fits_linear_family']}`",
        f"- full Sagrada ray fits family under tested scope: `{conclusion['full_sagrada_ray_fits_family_under_tested_scope']}`",
        "",
        "The source Durer-complement square is exactly in the displayed family",
        "in the identity orientation.  The Sagrada perturbation direction is not",
        "in the family's linear tangent space under the tested transform scope,",
        "so the bounded Sagrada ray is not a specialization of this family in",
        "the tested sense.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_morse_hedlund_family_fit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "morse_hedlund_family_fit.json"
        report_path = root / "results" / "MORSE_HEDLUND_FAMILY_FIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        print(json.dumps({"fit_counts": result["fit_counts"], "conclusion": result["conclusion"], "identity": result["identity_orientation"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
