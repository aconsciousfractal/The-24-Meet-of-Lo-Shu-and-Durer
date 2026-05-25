"""Compare subgroup/coset tilers with Type-A poset cones in S4.

For every labeled poset on {0,1,2,3}, compute its linear-extension set L(P).
Then test whether the left translates of L(P) can tile S4.  This gives a
small exact comparison class for the non-poset subgroup tilers D4 and V4.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

import analyze_s4_chambers as chambers


Relation = tuple[int, int]
RelationSet = frozenset[Relation]
Perm = chambers.Perm


ORDERED_PAIRS = tuple((a, b) for a in range(4) for b in range(4) if a != b)


def relation_string(relations: RelationSet) -> str:
    return ",".join(f"{a}<{b}" for a, b in sorted(relations))


def is_strict_poset(relations: RelationSet) -> bool:
    for a, b in relations:
        if (b, a) in relations:
            return False
    for a, b in relations:
        for c, d in relations:
            if b == c and a != d and (a, d) not in relations:
                return False
    return True


@lru_cache(maxsize=1)
def all_labeled_posets() -> tuple[RelationSet, ...]:
    out = []
    for mask in range(1 << len(ORDERED_PAIRS)):
        rels = frozenset(
            ORDERED_PAIRS[i] for i in range(len(ORDERED_PAIRS)) if mask & (1 << i)
        )
        if is_strict_poset(rels):
            out.append(rels)
    return tuple(sorted(out, key=lambda r: (len(r), relation_string(r))))


def linear_extensions(relations: RelationSet) -> tuple[Perm, ...]:
    exts = []
    for word in chambers.all_perms():
        if all(word.index(a) < word.index(b) for a, b in relations):
            exts.append(word)
    return tuple(exts)


def translated_subset(left: Perm, subset: frozenset[Perm]) -> frozenset[Perm]:
    return frozenset(chambers.compose(left, p) for p in subset)


def exact_left_tiling(subset: frozenset[Perm]) -> dict[str, Any]:
    universe = frozenset(chambers.all_perms())
    size = len(subset)
    if len(universe) % size != 0:
        return {"is_left_tiler": False, "reason": "size does not divide 24"}

    translates: dict[str, frozenset[Perm]] = {}
    for g in chambers.all_perms():
        translates[chambers.perm_string(g)] = translated_subset(g, subset)

    unique_translates: dict[frozenset[Perm], str] = {}
    for name, trans in translates.items():
        unique_translates.setdefault(trans, name)

    translate_items = [(name, trans) for trans, name in unique_translates.items()]
    covers_by_element: dict[Perm, list[int]] = defaultdict(list)
    for idx, (_, trans) in enumerate(translate_items):
        for p in trans:
            covers_by_element[p].append(idx)

    target_count = len(universe) // size

    def search(uncovered: frozenset[Perm], chosen: list[int]) -> list[int] | None:
        if not uncovered:
            return chosen
        if len(chosen) >= target_count:
            return None
        pivot = min(uncovered, key=lambda p: len(covers_by_element[p]))
        for idx in covers_by_element[pivot]:
            name, trans = translate_items[idx]
            if not trans <= uncovered:
                continue
            result = search(frozenset(uncovered - trans), chosen + [idx])
            if result is not None:
                return result
        return None

    solution = search(universe, [])
    if solution is None:
        return {
            "is_left_tiler": False,
            "translate_count": len(unique_translates),
            "required_translate_count": target_count,
        }

    selected = [
        {
            "left_multiplier": translate_items[idx][0],
            "words": [chambers.perm_string(p) for p in sorted(translate_items[idx][1])],
        }
        for idx in solution
    ]
    return {
        "is_left_tiler": True,
        "translate_count": len(unique_translates),
        "required_translate_count": target_count,
        "tiling": selected,
    }


def component_profile(subset: frozenset[Perm]) -> str:
    return str(tuple(len(component) for component in chambers.chamber_components(set(subset))))


def cone_record(words: tuple[Perm, ...], relations_examples: list[RelationSet]) -> dict[str, Any]:
    subset = frozenset(words)
    tiling = exact_left_tiling(subset)
    common_relations = chambers.common_precedence_relations(set(subset))
    closure = chambers.closure_from_relations(common_relations)
    return {
        "words": [chambers.perm_string(p) for p in sorted(subset)],
        "size": len(subset),
        "poset_count": len(relations_examples),
        "example_relations": relation_string(relations_examples[0]),
        "common_precedence_relations": common_relations,
        "is_standard_poset_cone": closure == set(subset),
        "chamber_graph": {
            "component_count": len(chambers.chamber_components(set(subset))),
            "component_sizes": [len(c) for c in chambers.chamber_components(set(subset))],
            "internal_edge_count": chambers.chamber_internal_edge_count(set(subset)),
            "boundary_edge_count": chambers.chamber_boundary_edge_count(set(subset)),
        },
        "left_tiling": tiling,
    }


def build_s4_poset_cone_comparison() -> dict:
    grouped: dict[tuple[str, ...], list[RelationSet]] = defaultdict(list)
    for rels in all_labeled_posets():
        words = tuple(chambers.perm_string(p) for p in linear_extensions(rels))
        grouped[words].append(rels)

    records = [
        cone_record(tuple(chambers.perm_from_string(w) for w in words), rels)
        for words, rels in sorted(grouped.items(), key=lambda item: (len(item[0]), item[0]))
    ]
    tilers = [record for record in records if record["left_tiling"]["is_left_tiler"]]
    size_counts = Counter(record["size"] for record in records)
    tiler_size_counts = Counter(record["size"] for record in tilers)
    component_counts = Counter(tuple(record["chamber_graph"]["component_sizes"]) for record in records)
    tiler_component_counts = Counter(
        tuple(record["chamber_graph"]["component_sizes"]) for record in tilers
    )

    d4_words = set(chambers.D4_WORDS)
    v4_words = set(chambers.V4_WORDS)

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase D",
            "description": "Enumeration of S4 poset cones L(P) and exact left-tiler comparison.",
        },
        "labeled_poset_count": len(all_labeled_posets()),
        "unique_linear_extension_set_count": len(records),
        "size_distribution": {str(k): size_counts[k] for k in sorted(size_counts)},
        "left_tiler_count": len(tilers),
        "left_tiler_size_distribution": {
            str(k): tiler_size_counts[k] for k in sorted(tiler_size_counts)
        },
        "component_size_distribution": {
            str(k): component_counts[k] for k in sorted(component_counts, key=str)
        },
        "left_tiler_component_size_distribution": {
            str(k): tiler_component_counts[k] for k in sorted(tiler_component_counts, key=str)
        },
        "D4_or_V4_as_poset_cone": {
            "D4": any(set(record["words"]) == d4_words for record in records),
            "V4": any(set(record["words"]) == v4_words for record in records),
        },
        "left_tilers": tilers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write S4 poset-cone comparison JSON")
    args = parser.parse_args()

    result = build_s4_poset_cone_comparison()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        path = root / "results" / "s4_poset_cone_comparison.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path)
    else:
        summary = dict(result)
        summary["left_tilers_sample"] = summary["left_tilers"][:8]
        summary["left_tilers"] = f"{len(result['left_tilers'])} records omitted; run with --write for full JSON"
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
