from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_inside_out_main_signature_split.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_inside_out_main_signature_split", SCRIPT)
split = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(split)


def test_main_signature_splits_as_144_plus_32():
    result = split.build_main_signature_split()
    assert result["main_pair_count"] == 176
    assert result["exact_v4_pair_count"] == 144
    assert result["extra_pair_count"] == 32


def test_exact_v4_part_has_canonical_terminal_set_and_source_types():
    result = split.build_main_signature_split()
    exact = result["exact_v4_summary"]
    assert exact["terminal_set_counts"] == {"0123,1032,2301,3210": 144}
    assert exact["terminal_order_profile_counts"] == {"1:1,2:3": 144}
    assert exact["source_type_counts"] == {"S1": 96, "S2": 16, "S3": 16, "S4": 16}
    assert exact["family_flag_counts"]["associated"] == 16
    assert exact["family_flag_counts"]["most_perfect_proxy"] == 16


def test_extra_32_are_subgroup_terminal_but_not_named_branch_members():
    result = split.build_main_signature_split()
    extra = result["extra_summary"]
    assert extra["pair_count"] == 32
    assert extra["terminal_subgroup_counts"] == {"True": 32}
    assert extra["selected_value_signature_counts"] == {"(11, 12, 15, 16)": 32}
    assert extra["source_type_counts"] == {"outside_exact_v4_source_types": 32}
    assert extra["family_flag_counts"]["associated"] == 0
    assert extra["family_flag_counts"]["panmagic"] == 0
    assert extra["family_flag_counts"]["most_perfect_proxy"] == 0
    assert extra["family_flag_counts"]["complement_fixed"] == 8


def test_extra_32_terminal_set_split():
    result = split.build_main_signature_split()
    extra = result["extra_summary"]
    assert extra["terminal_set_counts"] == {
        "0123,0213,3120,3210": 8,
        "0123,1302,2031,3210": 8,
        "0123,3210": 16,
    }
    assert extra["terminal_diagonal_size_counts"] == {"2": 16, "4": 16}
    assert extra["terminal_order_profile_counts"] == {
        "1:1,2:1": 16,
        "1:1,2:1,4:2": 8,
        "1:1,2:3": 8,
    }


def test_extra_32_source_diagonal_and_apd_split():
    result = split.build_main_signature_split()
    extra = result["extra_summary"]
    assert extra["source_diagonal_size_counts"] == {"2": 12, "4": 20}
    assert extra["apd_counts"] == {
        "(0,0,-9216,-1253376)": 4,
        "(0,0,-9216,-1256448)": 4,
        "(0,0,0,141312)": 4,
        "(0,0,0,156672)": 4,
        "(0,0,12288,1671168)": 8,
        "(0,0,3072,417792)": 8,
    }
