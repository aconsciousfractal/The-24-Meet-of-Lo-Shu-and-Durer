from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_morse_hedlund_family_fit.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_morse_hedlund_family_fit", SCRIPT)
family_fit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(family_fit)


def test_durer_complement_source_fits_morse_hedlund_family_in_identity_orientation():
    result = family_fit.build_morse_hedlund_family_fit()
    identity = result["identity_orientation"]
    assert identity["source_in_family"] is True
    assert identity["source_parameters"] == {
        "a": 14,
        "b": 15,
        "c": 16,
        "d": 13,
        "k1": -4,
        "k2": -8,
        "magic_sum": 34,
    }


def test_sagrada_terminal_and_direction_do_not_fit_family_in_identity_orientation():
    result = family_fit.build_morse_hedlund_family_fit()
    identity = result["identity_orientation"]
    assert identity["terminal_in_family"] is False
    assert identity["negative_mask_direction_in_linear_family"] is False
    assert identity["ray_in_family"] is False


def test_family_fit_counts_under_tested_transform_scope():
    result = family_fit.build_morse_hedlund_family_fit()
    assert result["metadata"]["transform_count"] == 2304
    assert result["fit_counts"] == {
        "source": 256,
        "terminal": 0,
        "direction": 0,
        "ray": 0,
    }


def test_full_sagrada_ray_is_not_morse_hedlund_specialization():
    result = family_fit.build_morse_hedlund_family_fit()
    assert result["conclusion"] == {
        "source_fits_family": True,
        "terminal_fits_family": False,
        "direction_fits_linear_family": False,
        "full_sagrada_ray_fits_family_under_tested_scope": False,
    }
    assert result["first_source_fit"] is not None
    assert result["first_terminal_fit"] is None
    assert result["first_direction_fit"] is None
    assert result["first_ray_fit"] is None
