from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_extra32_post_j2.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_extra32_post_j2", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_extra32_post_j2_counts_and_classes():
    result = audit.build_extra32_post_j2_audit()
    summary = result["summary"]
    assert summary["extra_pair_count"] == 32
    assert summary["terminal_set_class_distribution"] == {
        "two_diagonal_pair": 16,
        "v4_like_0213": 8,
        "v4_like_1302": 8,
    }
    assert len(result["records"]) == 32


def test_affine_defect_support_is_small_but_not_mask():
    result = audit.build_extra32_post_j2_audit()
    summary = result["summary"]
    assert summary["mismatch_support_is_mask_count"] == 0
    assert summary["mismatch_mask_intersection_distribution"] == {"0": 22, "2": 10}
    for record in result["records"]:
        assert len(record["mismatch_cells"]) == 4


def test_markov_and_hilbert_refine_but_do_not_collapse_extras():
    result = audit.build_extra32_post_j2_audit()
    summary = result["summary"]
    assert summary["markov_degree_distribution"] == {"0": 12, "1": 20}
    assert summary["hilbert_min_atom_count_distribution"] == {
        "12": 4,
        "14": 8,
        "16": 4,
        "18": 12,
        "20": 4,
    }
    assert len(summary["markov_component_profile_distribution"]) > 1
