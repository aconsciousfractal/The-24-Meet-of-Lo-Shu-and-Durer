from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_sagrada_terminal_retraction_shadow.py"

spec = importlib.util.spec_from_file_location("sagrada_terminal_retraction_shadow", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def data():
    return module.build_certificate()


def test_terminal_is_finite_retraction():
    cert = data()
    assert cert["claims"]["terminal_is_retraction_of_source"] is True
    assert cert["claims"]["retraction_image_size_is_12"] is True
    assert cert["retraction"]["fiber_size_distribution"] == {1: 8, 2: 4}
    assert cert["retraction"]["sagrada_plane"] == ["0010", "0100", "1001", "1111"]
    assert [row["to"] for row in cert["retraction"]["fold_pairs"]] == ["1011", "1101", "0000", "0110"]


def test_duplicate_fibers_recover_direction():
    cert = data()
    assert cert["terminal_duplicate_direction"]["duplicate_values"] == [1, 2, 5, 6]
    assert cert["terminal_duplicate_direction"]["duplicate_directions"] == ["1001"]
    assert cert["claims"]["duplicate_direction_is_terminally_recovered_u"] is True


def test_quaterne_count_shadow_is_guarded():
    cert = data()
    assert cert["claims"]["h24_count_is_96"] is True
    assert cert["claims"]["affine_nonaffine_split_is_36_60"] is True
    assert cert["claims"]["nonaffine_count_shadow_is_32_12_16"] is True
    assert cert["terminal_quaternes"]["shadow_count_vector_numeric"] == [32, 12, 16]
    assert cert["terminal_quaternes"]["shadow_count_vector"] == {
        "CS1_mixed_single_direction": 32,
        "CS2_pure_nonfull_direction": 12,
        "CS3_pure_full_direction": 16,
    }
    assert cert["claims"]["no_b3_identification_claim"] is True