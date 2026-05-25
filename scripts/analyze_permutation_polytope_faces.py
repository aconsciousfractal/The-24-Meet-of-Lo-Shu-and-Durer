"""Face tests and f-vectors for the D4/V4 permutation polytopes."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from scipy.optimize import linprog

import analyze_permutation_polytope_bridge as pp


Perm = tuple[int, int, int, int]
Vector = tuple[int, ...]


def all_s4_perms() -> list[Perm]:
    return [tuple(p) for p in itertools.permutations(range(4))]  # type: ignore[list-item]


def vector(p: Perm) -> Vector:
    return tuple(pp.permutation_matrix_flat(p))


def vector_diff(left: Vector, right: Vector) -> list[int]:
    return [a - b for a, b in zip(left, right)]


def face_feasible(subset: list[Perm], vertices: list[Perm]) -> dict:
    subset_set = set(subset)
    outside = [p for p in vertices if p not in subset_set]
    if not subset:
        return {"is_face": True, "reason": "empty face"}
    if not outside:
        return {"is_face": True, "reason": "whole polytope"}

    base = vector(subset[0])
    a_eq = [vector_diff(vector(p), base) for p in subset[1:]]
    b_eq = [0] * len(a_eq)
    a_ub = [vector_diff(vector(p), base) for p in outside]
    b_ub = [-1] * len(a_ub)

    result = linprog(
        c=[0] * 16,
        A_ub=a_ub,
        b_ub=b_ub,
        A_eq=a_eq or None,
        b_eq=b_eq or None,
        bounds=[(None, None)] * 16,
        method="highs",
    )
    return {
        "is_face": bool(result.success),
        "reason": "supporting functional exists" if result.success else "no supporting functional",
        "linprog_status": int(result.status),
        "linprog_message": result.message,
    }


def affine_dimension(perms: list[Perm]) -> int:
    if len(perms) <= 1:
        return 0
    return pp.permutation_polytope_dimension(perms)


def face_lattice_summary(vertices: list[Perm]) -> dict:
    faces = []
    vertex_list = sorted(vertices)
    for size in range(1, len(vertex_list) + 1):
        for subset in itertools.combinations(vertex_list, size):
            subset_list = list(subset)
            feasible = face_feasible(subset_list, vertex_list)
            if feasible["is_face"]:
                faces.append(
                    {
                        "words": [pp.perm_string(p) for p in subset_list],
                        "size": len(subset_list),
                        "dimension": affine_dimension(subset_list),
                    }
                )
    f_vector = Counter(face["dimension"] for face in faces)
    return {
        "vertex_count": len(vertex_list),
        "polytope_dimension": affine_dimension(vertex_list),
        "proper_nonempty_face_count": sum(1 for face in faces if face["size"] < len(vertex_list)),
        "nonempty_face_count_including_whole": len(faces),
        "f_vector_nonempty_including_whole": {
            str(dim): f_vector[dim] for dim in sorted(f_vector)
        },
        "f_vector": {
            str(dim): f_vector[dim]
            for dim in sorted(f_vector)
            if dim < affine_dimension(vertex_list)
        },
        "faces_by_dimension": {
            str(dim): [
                face["words"]
                for face in faces
                if face["dimension"] == dim and face["size"] < len(vertex_list)
            ]
            for dim in sorted(f_vector)
            if dim < affine_dimension(vertex_list)
        },
    }


def support_positions(perms: list[Perm]) -> set[tuple[int, int]]:
    return {(i, p[i]) for p in perms for i in range(4)}


def permutations_inside_support(support: set[tuple[int, int]]) -> list[Perm]:
    return [
        p
        for p in all_s4_perms()
        if all((i, p[i]) in support for i in range(4))
    ]


def birkhoff_face_test(perms: list[Perm]) -> dict:
    support = support_positions(perms)
    completion = permutations_inside_support(support)
    is_face_vertex_set = set(completion) == set(perms)
    return {
        "support_size": len(support),
        "support_positions": [f"{i},{j}" for i, j in sorted(support)],
        "birkhoff_face_completion_size": len(completion),
        "birkhoff_face_completion_words": [pp.perm_string(p) for p in sorted(completion)],
        "is_birkhoff_face_vertex_set": is_face_vertex_set,
        "is_birkhoff_proper_face": is_face_vertex_set and len(completion) < 24,
        "reason": (
            "vertex set equals all permutations supported on the union support"
            if is_face_vertex_set
            else "support completion contains additional permutation vertices"
        ),
    }


def build_permutation_polytope_face_audit() -> dict:
    bridge = pp.build_permutation_polytope_bridge()
    d4 = [pp.perm_from_string(word) for word in bridge["subsets"]["D4"]["words"]]
    v4 = [pp.perm_from_string(word) for word in bridge["subsets"]["V4"]["words"]]
    all_perms = all_s4_perms()
    v4_cosets = [
        [pp.perm_from_string(word) for word in row["words"]]
        for row in bridge["cosets"]["V4"]
    ]
    d4_cosets = [
        [pp.perm_from_string(word) for word in row["words"]]
        for row in bridge["cosets"]["D4"]
    ]

    v4_in_d4 = face_feasible(v4, d4)
    d4_in_b4_lp = face_feasible(d4, all_perms)
    v4_in_b4_lp = face_feasible(v4, all_perms)
    d4_birkhoff = birkhoff_face_test(d4)
    v4_birkhoff = birkhoff_face_test(v4)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase G permutation-polytope face audit",
            "description": "Face tests and f-vectors for P(D4), P(V4), and their Birkhoff placement.",
        },
        "face_tests": {
            "P_V4_is_face_of_P_D4": v4_in_d4,
            "P_D4_is_face_of_B4_lp": d4_in_b4_lp,
            "P_V4_is_face_of_B4_lp": v4_in_b4_lp,
            "P_D4_is_birkhoff_face_by_support": d4_birkhoff,
            "P_V4_is_birkhoff_face_by_support": v4_birkhoff,
        },
        "f_vectors": {
            "P_D4": face_lattice_summary(d4),
            "P_V4": face_lattice_summary(v4),
        },
        "coset_face_tests": {
            "V4_cosets_in_B4_by_support": [
                {
                    "index": index,
                    **birkhoff_face_test(coset),
                }
                for index, coset in enumerate(v4_cosets)
            ],
            "D4_cosets_in_B4_by_support": [
                {
                    "index": index,
                    **birkhoff_face_test(coset),
                }
                for index, coset in enumerate(d4_cosets)
            ],
        },
        "conclusion": {
            "P_V4_is_face_of_P_D4": v4_in_d4["is_face"],
            "P_D4_is_face_of_B4": d4_birkhoff["is_birkhoff_face_vertex_set"],
            "P_V4_is_face_of_B4": v4_birkhoff["is_birkhoff_face_vertex_set"],
            "P_D4_f_vector": face_lattice_summary(d4)["f_vector"],
            "P_V4_f_vector": face_lattice_summary(v4)["f_vector"],
        },
    }


def write_report(result: dict, path: Path) -> None:
    tests = result["face_tests"]
    f_d4 = result["f_vectors"]["P_D4"]
    f_v4 = result["f_vectors"]["P_V4"]
    lines = [
        "# Permutation-Polytope Face Audit",
        "",
        "Status: Phase G face-test branch",
        "",
        "## Face Tests",
        "",
        f"- `P(V4)` face of `P(D4)`: `{tests['P_V4_is_face_of_P_D4']['is_face']}`",
        f"- `P(D4)` Birkhoff face by support: `{tests['P_D4_is_birkhoff_face_by_support']['is_birkhoff_face_vertex_set']}`",
        f"- `P(V4)` Birkhoff face by support: `{tests['P_V4_is_birkhoff_face_by_support']['is_birkhoff_face_vertex_set']}`",
        "",
        "## F-Vectors",
        "",
        f"- `P(D4)` dimension: `{f_d4['polytope_dimension']}`",
        f"- `P(D4)` f-vector: `{f_d4['f_vector']}`",
        f"- `P(V4)` dimension: `{f_v4['polytope_dimension']}`",
        f"- `P(V4)` f-vector: `{f_v4['f_vector']}`",
        "",
        "## Birkhoff Support Completion",
        "",
        f"- `D4` support size: `{tests['P_D4_is_birkhoff_face_by_support']['support_size']}`",
        f"- `D4` completion size: `{tests['P_D4_is_birkhoff_face_by_support']['birkhoff_face_completion_size']}`",
        f"- `V4` support size: `{tests['P_V4_is_birkhoff_face_by_support']['support_size']}`",
        f"- `V4` completion size: `{tests['P_V4_is_birkhoff_face_by_support']['birkhoff_face_completion_size']}`",
        "",
        "## Interpretation",
        "",
        "`P(V4)` is a natural subpolytope of `P(D4)`, but it is not a face of",
        "`P(D4)` under this vertex set.  Neither `P(D4)` nor `P(V4)` is a face",
        "of the full Birkhoff polytope `B4`: their union supports allow all 24",
        "permutation vertices.  The correct statement is therefore a subgroup",
        "subpolytope / Birkhoff-skeleton statement, not a face statement.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_permutation_polytope_face_audit()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "permutation_polytope_face_audit.json"
        report_path = root / "results" / "PERMUTATION_POLYTOPE_FACE_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        print(json.dumps(result["conclusion"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
