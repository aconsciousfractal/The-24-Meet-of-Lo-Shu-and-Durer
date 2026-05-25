from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_apd_pte.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_apd_pte", SCRIPT)
apd_pte = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(apd_pte)


def test_apd_pte_polynomial_layer():
    result = apd_pte.build_apd_pte_analysis()
    assert result["apd_zero_polynomials"] == ["1", "2"]
    assert result["apd_polynomials_coefficients_ascending"]["3"] == [
        0,
        -1536,
        480,
        -24,
    ]
    assert result["apd3_factorization"] == "-24*t*(t-4)*(t-16)"


def test_first_nonzero_degrees_on_sagrada_interval():
    result = apd_pte.build_apd_pte_analysis()
    first = result["bounded_interval_first_nonzero_degree"]
    assert first["0"] == 4
    assert first["4"] == 4
    assert first["10"] == 3
    for t in ("1", "2", "3", "5", "6", "7", "8", "9"):
        assert first[t] == 3


def test_terminal_is_not_apd_zero_point():
    result = apd_pte.build_apd_pte_analysis()
    terminal = result["special_t_records"]["10"]
    assert terminal["magic_sum"] == 24
    assert terminal["inside_bounded_sagrada_interval"] is True
    assert terminal["apd_values"]["3"] != 0
    assert terminal["first_nonzero_degree_up_to_max"] == 3


def test_internal_and_external_apd3_roots_are_not_terminal_endpoint():
    result = apd_pte.build_apd_pte_analysis()
    internal = result["special_t_records"]["4"]
    external = result["special_t_records"]["16"]
    assert internal["apd_values"]["3"] == 0
    assert internal["magic_sum"] == 30
    assert internal["inside_bounded_sagrada_interval"] is True
    assert external["apd_values"]["3"] == 0
    assert external["inside_bounded_sagrada_interval"] is False
