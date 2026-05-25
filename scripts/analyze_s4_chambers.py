"""Type-A / S4 chamber fingerprints for D4 and V4.

The chambers of the Coxeter complex A3 are indexed by the 24 permutations in
S4.  Phase D treats the Durer source diagonal set D4 and terminal diagonal set
V4 as chamber unions.

This script records:

- subgroup and coset data;
- common-halfspace / poset-cone closure data;
- chamber-graph connectivity data.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, deque
from pathlib import Path


Perm = tuple[int, int, int, int]

D4_WORDS = ("0123", "0213", "1032", "1302", "2031", "2301", "3120", "3210")
V4_WORDS = ("0123", "1032", "2301", "3210")


def perm_from_string(text: str) -> Perm:
    return tuple(int(c) for c in text)  # type: ignore[return-value]


def perm_string(p: Perm) -> str:
    return "".join(str(x) for x in p)


def all_perms() -> tuple[Perm, ...]:
    return tuple(itertools.permutations(range(4)))  # type: ignore[return-value]


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
    raise ValueError(f"order search exceeded for {p!r}")


def order_profile(perms: set[Perm]) -> dict[str, int]:
    counts = Counter(perm_order(p) for p in perms)
    return {str(k): counts[k] for k in sorted(counts)}


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


def left_cosets(subgroup: set[Perm]) -> list[list[str]]:
    remaining = set(all_perms())
    cosets = []
    while remaining:
        g = min(remaining)
        coset = {compose(g, h) for h in subgroup}
        cosets.append([perm_string(p) for p in sorted(coset)])
        remaining -= coset
    return cosets


def common_precedence_relations(words: set[Perm]) -> list[str]:
    relations = []
    for a in range(4):
        for b in range(4):
            if a == b:
                continue
            if all(word.index(a) < word.index(b) for word in words):
                relations.append(f"{a}<{b}")
    return sorted(relations)


def closure_from_relations(relations: list[str]) -> set[Perm]:
    pairs = [(int(rel[0]), int(rel[2])) for rel in relations]
    return {
        p for p in all_perms()
        if all(p.index(a) < p.index(b) for a, b in pairs)
    }


def adjacent_words(word: Perm) -> list[Perm]:
    out = []
    for i in range(3):
        row = list(word)
        row[i], row[i + 1] = row[i + 1], row[i]
        out.append(tuple(row))  # type: ignore[arg-type]
    return out


def chamber_components(subset: set[Perm]) -> list[list[str]]:
    remaining = set(subset)
    components = []
    while remaining:
        start = min(remaining)
        queue: deque[Perm] = deque([start])
        seen = {start}
        remaining.remove(start)
        while queue:
            current = queue.popleft()
            for nxt in adjacent_words(current):
                if nxt not in subset or nxt in seen:
                    continue
                seen.add(nxt)
                remaining.remove(nxt)
                queue.append(nxt)
        components.append([perm_string(p) for p in sorted(seen)])
    return components


def chamber_boundary_edge_count(subset: set[Perm]) -> int:
    count = 0
    for p in subset:
        for nxt in adjacent_words(p):
            if nxt not in subset:
                count += 1
    return count


def chamber_internal_edge_count(subset: set[Perm]) -> int:
    count = 0
    for p in subset:
        for nxt in adjacent_words(p):
            if nxt in subset:
                count += 1
    return count // 2


def fingerprint(name: str, words: tuple[str, ...]) -> dict:
    subset = {perm_from_string(word) for word in words}
    relations = common_precedence_relations(subset)
    closure = closure_from_relations(relations)
    components = chamber_components(subset)
    cosets = left_cosets(subset) if is_subgroup(subset) else []
    return {
        "name": name,
        "words": [perm_string(p) for p in sorted(subset)],
        "size": len(subset),
        "is_subgroup": is_subgroup(subset),
        "order_profile": order_profile(subset),
        "left_coset_count": len(cosets),
        "left_cosets": cosets,
        "common_precedence_relations": relations,
        "common_halfspace_closure_size": len(closure),
        "common_halfspace_closure_words": [perm_string(p) for p in sorted(closure)],
        "is_standard_poset_cone": closure == subset,
        "chamber_graph": {
            "component_count": len(components),
            "components": components,
            "component_sizes": [len(component) for component in components],
            "internal_edge_count": chamber_internal_edge_count(subset),
            "boundary_edge_count": chamber_boundary_edge_count(subset),
        },
    }


def build_s4_chamber_fingerprints() -> dict:
    d4 = fingerprint("D4_source_diagonals", D4_WORDS)
    v4 = fingerprint("V4_terminal_diagonals", V4_WORDS)
    all_chambers = set(all_perms())
    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase D",
            "description": "Type-A A3 chamber fingerprints for Durer D4 and terminal V4 permutation-diagonal sets.",
            "chamber_model": "A3 chambers are indexed by words in S4; chamber adjacency swaps adjacent positions in the word.",
        },
        "s4_size": len(all_chambers),
        "s4_chamber_edge_count": chamber_internal_edge_count(all_chambers),
        "subsets": {
            "D4": d4,
            "V4": v4,
        },
        "comparison": {
            "D4_contains_V4": set(perm_from_string(w) for w in V4_WORDS).issubset(
                set(perm_from_string(w) for w in D4_WORDS)
            ),
            "size_drop": f"{len(D4_WORDS)} -> {len(V4_WORDS)}",
            "coset_tiler_counts": {
                "D4": len(d4["left_cosets"]),
                "V4": len(v4["left_cosets"]),
            },
            "poset_cone_status": {
                "D4": d4["is_standard_poset_cone"],
                "V4": v4["is_standard_poset_cone"],
            },
            "chamber_component_counts": {
                "D4": d4["chamber_graph"]["component_count"],
                "V4": v4["chamber_graph"]["component_count"],
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write S4 chamber fingerprint JSON")
    args = parser.parse_args()

    result = build_s4_chamber_fingerprints()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "s4_chamber_fingerprints.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = {
            "s4_size": result["s4_size"],
            "s4_chamber_edge_count": result["s4_chamber_edge_count"],
            "comparison": result["comparison"],
            "D4": {
                "size": result["subsets"]["D4"]["size"],
                "order_profile": result["subsets"]["D4"]["order_profile"],
                "component_sizes": result["subsets"]["D4"]["chamber_graph"]["component_sizes"],
                "closure_size": result["subsets"]["D4"]["common_halfspace_closure_size"],
            },
            "V4": {
                "size": result["subsets"]["V4"]["size"],
                "order_profile": result["subsets"]["V4"]["order_profile"],
                "component_sizes": result["subsets"]["V4"]["chamber_graph"]["component_sizes"],
                "closure_size": result["subsets"]["V4"]["common_halfspace_closure_size"],
            },
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
