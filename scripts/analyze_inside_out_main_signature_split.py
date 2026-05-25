"""Split the 176-pair main Phase-H inside-out terminal signature."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import analyze_order4_named_families as families
import analyze_order4_terminal24 as terminal24
import analyze_order4_v4_subclass as v4
import enumerate_order4_endpoints as order4


MAIN_TERMINAL_PROFILE = {
    "edge_count": 107,
    "left_dependencies_Q": 91,
    "rank_F2": 14,
    "rank_Q": 16,
    "right_kernel_Q": 0,
    "snf_counts": {"1": 14, "2": 1, "20": 1},
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def counter_json(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def apd_key(apd: list[int]) -> str:
    return "(" + ",".join(str(x) for x in apd) + ")"


def terminal_set_key(values: list[str]) -> str:
    return ",".join(values)


def source_type_map() -> dict[tuple[str, ...], str]:
    rows = v4.classify_v4_subclass()["source_diagonal_types"]
    return {tuple(row["source_diagonal_set"]): row["type_id"] for row in rows}


def family_flags_by_square() -> dict[int, dict[str, bool]]:
    squares = order4.essential_order4_representatives()
    index_by_square = {square: idx for idx, square in enumerate(squares)}
    return {
        idx: families.family_flags(square, index_by_square, idx)
        for idx, square in enumerate(squares)
    }


def profile_matches_main(record: dict) -> bool:
    return record["terminal_profile"] == MAIN_TERMINAL_PROFILE


def summarize_group(records: list[dict]) -> dict:
    return {
        "pair_count": len(records),
        "square_count": len({record["square_index"] for record in records}),
        "mask_counts": counter_json(Counter(record["mask"] for record in records)),
        "selected_value_signature_counts": counter_json(
            Counter(tuple(record["sorted_values"]) for record in records)
        ),
        "apd_counts": counter_json(Counter(record["apd_vector"] for record in records)),
        "source_diagonal_size_counts": counter_json(
            Counter(len(record["source_diagonal_set"]) for record in records)
        ),
        "terminal_diagonal_size_counts": counter_json(
            Counter(len(record["terminal_diagonal_set"]) for record in records)
        ),
        "terminal_subgroup_counts": counter_json(
            Counter(record["terminal_diagonal_is_subgroup"] for record in records)
        ),
        "terminal_order_profile_counts": counter_json(
            Counter(
                record["terminal_diagonal_order_profile"]
                for record in records
                if record["terminal_diagonal_order_profile"] is not None
            )
        ),
        "terminal_set_counts": counter_json(
            Counter(terminal_set_key(record["terminal_diagonal_set"]) for record in records)
        ),
        "source_type_counts": counter_json(
            Counter(record["source_type"] for record in records)
        ),
        "family_flag_counts": {
            name: sum(1 for record in records if record["family_flags"][name])
            for name in sorted(records[0]["family_flags"]) if records
        },
        "square_indices": sorted({record["square_index"] for record in records}),
    }


@lru_cache(maxsize=1)
def build_main_signature_split() -> dict:
    root = Path(__file__).resolve().parents[1]
    inside_out = load_json(root / "results" / "order4_inside_out_profiles.json")
    terminal = load_json(root / "results" / "order4_terminal24_fingerprints.json")
    terminal_by_pair = {
        (record["square_index"], record["mask"]): record
        for record in terminal["records"]  # type: ignore[index]
    }
    source_types = source_type_map()
    flags = family_flags_by_square()

    main_records = []
    for profile_record in inside_out["records"]:  # type: ignore[index]
        if not profile_matches_main(profile_record):
            continue
        key = (profile_record["square_index"], profile_record["mask"])
        terminal_record = terminal_by_pair[key]
        source_set = tuple(terminal_record["source_diagonal_set"])
        enriched = {
            **profile_record,
            "apd_vector": apd_key(terminal_record["apd_vector"]),
            "values": terminal_record["values"],
            "source_diagonal_set": terminal_record["source_diagonal_set"],
            "terminal_diagonal_set": terminal_record["terminal_diagonal_set"],
            "source_type": source_types.get(source_set, "outside_exact_v4_source_types"),
            "family_flags": flags[profile_record["square_index"]],
        }
        main_records.append(enriched)

    exact_v4 = [record for record in main_records if record["is_exact_canonical_v4"]]
    extra = [record for record in main_records if not record["is_exact_canonical_v4"]]

    by_source_type: dict[str, list[dict]] = defaultdict(list)
    for record in main_records:
        by_source_type[record["source_type"]].append(record)

    by_family = {}
    if main_records:
        for name in sorted(main_records[0]["family_flags"]):
            group = [record for record in main_records if record["family_flags"][name]]
            by_family[name] = summarize_group(group) if group else {"pair_count": 0}

    return {
        "metadata": {
            "project": "Magic 24",
            "phase": "Phase H main inside-out signature split",
            "description": "Split the 176-pair terminal signature edges=107, rank_F2=14, SNF=1^14,2,20 into exact-canonical-V4 and extra records.",
        },
        "main_terminal_profile": MAIN_TERMINAL_PROFILE,
        "main_pair_count": len(main_records),
        "exact_v4_pair_count": len(exact_v4),
        "extra_pair_count": len(extra),
        "main_summary": summarize_group(main_records),
        "exact_v4_summary": summarize_group(exact_v4),
        "extra_summary": summarize_group(extra),
        "source_type_summaries": {
            key: summarize_group(group)
            for key, group in sorted(by_source_type.items())
        },
        "family_summaries": by_family,
        "extra_records": extra,
    }


def write_report(result: dict, path: Path) -> None:
    lines = [
        "# Inside-Out Main Signature Split",
        "",
        "Status: Phase H refinement of the 176-pair main terminal signature",
        "",
        "## Summary",
        "",
        f"- main signature pairs: `{result['main_pair_count']}`",
        f"- exact canonical `V4` pairs: `{result['exact_v4_pair_count']}`",
        f"- extra non-exact-canonical-`V4` pairs: `{result['extra_pair_count']}`",
        f"- main profile: `{result['main_terminal_profile']}`",
        "",
        "## Exact V4 vs Extra",
        "",
        "Exact canonical `V4`:",
        "",
        f"`{result['exact_v4_summary']}`",
        "",
        "Extra non-exact-canonical `V4`:",
        "",
        f"`{result['extra_summary']}`",
        "",
        "## Source Types",
        "",
    ]
    for name, summary in result["source_type_summaries"].items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"`{summary}`")
        lines.append("")
    lines.extend(["## Family Slices", ""])
    for name, summary in result["family_summaries"].items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"`{summary}`")
        lines.append("")
    lines.extend(
        [
            "## Interpretation",
            "",
            "The main inside-out signature is exactly the selected-mask-affine",
            "terminal-24 class, but it is broader than exact canonical `V4`.",
            "The split report identifies the 32 extra pairs explicitly so the next",
            "Phase-H branch can test whether a finer source-type, family,",
            "automorphism, Hilbert, or Markov invariant separates them.",
            "",
            "## Guardrail",
            "",
            "This is a stratification report.  It still does not prove a Hilbert",
            "or Markov characterization of Durer/Sagrada.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = build_main_signature_split()
    if args.write:
        root = Path(__file__).resolve().parents[1]
        json_path = root / "results" / "inside_out_main_signature_split.json"
        report_path = root / "results" / "INSIDE_OUT_MAIN_SIGNATURE_SPLIT_REPORT.md"
        json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(result, report_path)
        print(json_path)
        print(report_path)
    else:
        summary = {
            "main_pair_count": result["main_pair_count"],
            "exact_v4_pair_count": result["exact_v4_pair_count"],
            "extra_pair_count": result["extra_pair_count"],
            "extra_summary": result["extra_summary"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
