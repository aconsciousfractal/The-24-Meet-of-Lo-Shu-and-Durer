from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_hilbert_semigroup_audit.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_hilbert_semigroup_audit", SCRIPT)
hilbert = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(hilbert)


def test_checked_atom_counts_are_stable():
    result = hilbert.build_hilbert_semigroup_audit()
    assert result["atom_check_max_sum"] == 8
    assert result["atom_count_total"] == 20
    assert result["atom_counts_by_sum"] == {
        "1": 8,
        "2": 12,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
    }
    assert result["atom_magic_sum_distribution"] == {"1": 8, "2": 12}


def test_small_sum_square_counts_are_stable():
    result = hilbert.build_hilbert_semigroup_audit()
    assert result["square_counts_by_sum"] == {
        "1": 8,
        "2": 48,
        "3": 200,
        "4": 675,
        "5": 1904,
        "6": 4736,
        "7": 10608,
        "8": 21925,
    }


def test_durer_source_and_terminal_decompose_in_checked_atoms():
    result = hilbert.build_hilbert_semigroup_audit()
    source = result["named_decompositions"]["durer_source_D"]["decomposition"]
    terminal = result["named_decompositions"]["durer_terminal_D10"]["decomposition"]
    assert source["success"] is True
    assert source["reconstruction_matches"] is True
    assert source["min_atom_count"] == 18
    assert source["atom_magic_sum_coefficient_counts"] == {"1": 2, "2": 16}
    assert terminal["success"] is True
    assert terminal["reconstruction_matches"] is True
    assert terminal["min_atom_count"] == 18
    assert terminal["atom_magic_sum_coefficient_counts"] == {"1": 12, "2": 6}


def test_all_terminal24_endpoints_decompose_in_checked_atoms():
    result = hilbert.build_hilbert_semigroup_audit()
    summary = result["terminal24_decomposition_summary"]
    assert summary["pair_count"] == 236
    assert summary["failed_decomposition_count"] == 0
    assert summary["min_atom_count_distribution"] == {
        "12": 4,
        "13": 4,
        "14": 24,
        "15": 8,
        "16": 44,
        "17": 16,
        "18": 100,
        "19": 8,
        "20": 20,
        "22": 8,
    }


def test_terminal24_class_min_atom_distributions_are_stable():
    result = hilbert.build_hilbert_semigroup_audit()
    by_class = result["terminal24_decomposition_summary"]["class_min_atom_count_distributions"]
    assert by_class["exact_v4"] == {"14": 16, "16": 24, "18": 80, "20": 16, "22": 8}
    assert by_class["main_extra"] == {"12": 4, "14": 8, "16": 4, "18": 12, "20": 4}
    assert by_class["outside_main"] == {
        "13": 4,
        "15": 8,
        "16": 16,
        "17": 16,
        "18": 8,
        "19": 8,
    }
