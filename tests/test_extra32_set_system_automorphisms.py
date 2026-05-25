from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_extra32_set_system_automorphisms.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_extra32_set_system_automorphisms", SCRIPT)
extra32 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(extra32)


def test_all_extra32_colored_set_systems_are_rigid():
    result = extra32.build_extra32_automorphism_audit()
    assert result["extra_pair_count"] == 32
    assert result["automorphism_tuple_counts"] == {"(1, 1, 1, 1)": 32}
    for record in result["records"]:
        assert record["automorphism_orders"] == {
            "lines_plus_mask": 1,
            "source": 1,
            "terminal": 1,
            "combined": 1,
        }


def test_extra32_terminal_set_classes_are_stable():
    result = extra32.build_extra32_automorphism_audit()
    summaries = result["terminal_set_class_summaries"]
    assert set(summaries) == {"two_diagonal_pair", "v4_like_0213", "v4_like_1302"}
    assert summaries["two_diagonal_pair"]["pair_count"] == 16
    assert summaries["v4_like_0213"]["pair_count"] == 8
    assert summaries["v4_like_1302"]["pair_count"] == 8


def test_extra32_two_diagonal_pair_class_contains_the_complement_fixed_records():
    result = extra32.build_extra32_automorphism_audit()
    summaries = result["terminal_set_class_summaries"]
    two_diag = summaries["two_diagonal_pair"]
    assert two_diag["complement_fixed_count"] == 8
    assert two_diag["source_diagonal_size_counts"] == {"2": 12, "4": 4}
    assert summaries["v4_like_0213"]["complement_fixed_count"] == 0
    assert summaries["v4_like_1302"]["complement_fixed_count"] == 0


def test_extra32_v4_like_classes_have_source_size_four():
    result = extra32.build_extra32_automorphism_audit()
    summaries = result["terminal_set_class_summaries"]
    assert summaries["v4_like_0213"]["source_diagonal_size_counts"] == {"4": 8}
    assert summaries["v4_like_1302"]["source_diagonal_size_counts"] == {"4": 8}
