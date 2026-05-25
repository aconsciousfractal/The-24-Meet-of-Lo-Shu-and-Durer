from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "enumerate_order4_endpoints.py"

spec = importlib.util.spec_from_file_location("enumerate_order4_endpoints", SCRIPT)
order4 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(order4)


def test_internal_order4_dataset_counts():
    raw = order4.generate_order4_normal_magic_squares()
    essential = order4.essential_order4_representatives()
    assert len(raw) == 7040
    assert len(essential) == 880
    assert all(order4.is_magic(square) for square in essential)


def test_canonical_orbit_size_is_eight_for_normal_squares():
    essential = order4.essential_order4_representatives()
    for square in essential[:25]:
        assert len(set(order4.symmetry_orbit(square))) == 8


def test_durer_complement_sagrada_endpoint_is_present():
    durer = (
        (1, 14, 15, 4),
        (12, 7, 6, 9),
        (8, 11, 10, 5),
        (13, 2, 3, 16),
    )
    canonical = order4.canonical_square(durer)
    assert canonical in order4.essential_order4_representatives()
    endpoint = order4.endpoint_for_mask(durer, (2, 0, 1, 3))
    assert endpoint["values"] == [15, 12, 11, 16]
    assert endpoint["t_max"] == 10
    assert endpoint["terminal_sum"] == 24


def test_endpoint_spectrum_internal_consistency():
    essential = order4.essential_order4_representatives()
    spectrum = order4.endpoint_spectrum_for_squares(essential)
    assert spectrum["square_count"] == 880
    assert spectrum["admissible_mask_count"] == 8
    assert spectrum["pair_count"] == 7040
    assert sum(spectrum["terminal_sum_counts"].values()) == 7040
    assert spectrum["terminal_24_pair_count"] == sum(
        spectrum["terminal_24_mask_counts"].values()
    )
