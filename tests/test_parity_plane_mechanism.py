from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_parity_plane_mechanism.py"
DOC = ROOT / "docs" / "PARITY_PLANE_MECHANISM.md"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_parity_plane_mechanism", SCRIPT)
parity = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(parity)


def test_affine_plane_sum_lemma_exhaustive():
    for u in range(1, 16):
        for w in range(1, 16):
            if u == w:
                continue
            labels = [0, u, w, u ^ w]
            expected = sum(labels) == 30
            assert parity.affine_plane_sum_is_balanced(u, w) == expected


def test_public_residual_table_matches_expected_values():
    data = parity.build_parity_plane_mechanism()
    table = {row["v"]: row for row in data["finite_residual_table"]}
    expected = {
        2: (0, 8, 64, [2], [12, 14]),
        4: (1, 8, 64, [4], [9, 13]),
        6: (0, 16, 64, [6], [8, 10, 12, 14]),
        8: (2, 8, 64, [8], [3, 11]),
        12: (1, 16, 64, [12], [1, 5, 9, 13]),
        14: (0, 24, 48, [14], [2, 4, 6, 8, 10, 12]),
    }
    assert set(table) == set(expected)
    for v, (critical_bit, direction_count, offset_count, a_values, g_values) in expected.items():
        row = table[v]
        assert row["critical_bit"] == critical_bit
        assert row["direction_survivor_count"] == direction_count
        assert row["offset_survivor_count"] == offset_count
        assert row["a_values"] == a_values
        assert row["g_values"] == g_values
        assert row["a_equals_v_for_all_survivors"] is True
        assert row["g_has_zero_critical_bit_for_all_survivors"] is True
        assert row["nw_bit_balance_possible"] is False


def test_public_summary_and_guardrails_are_scoped():
    data = parity.build_parity_plane_mechanism()
    summary = data["summary"]
    assert summary["all_survivors_have_a_equals_v"] is True
    assert summary["all_survivors_have_g_zero_on_critical_bit"] is True
    assert summary["nw_bit_balance_possible_in_row_residual"] is False
    assert summary["column_residual_by_transpose_symmetry"] is True
    assert summary["proof_status"] == "finite_residual_check_with_six_values_not_table_free"
    assert any("not a table-free" in item for item in data["guardrails"])
    assert any("not a universal" in item for item in data["guardrails"])


def test_public_doc_has_no_internal_level_names():
    text = DOC.read_text(encoding="utf-8")
    assert "Parity-plane mechanism" in text
    assert "B11" in text
    assert "six-value finite check" in text
    for suffix in range(30, 36):
        assert f"L{suffix}" not in text