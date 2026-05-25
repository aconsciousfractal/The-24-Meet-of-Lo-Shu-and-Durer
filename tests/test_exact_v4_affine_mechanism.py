from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_exact_v4_affine_mechanism.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_exact_v4_affine_mechanism", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_exact_v4_is_full_translation_v4():
    result = audit.build_exact_v4_affine_mechanism_audit()
    mechanism = result["linear_mechanism"]
    assert result["exact_canonical_v4_pair_count"] == 144
    assert result["selected_affine_extra_count"] == 32
    assert mechanism["exact_v4_terminal_sets_full_translation_v4"] == 144
    assert mechanism["exact_v4_all_terminal_sets_full_translation_v4"] is True
    assert mechanism["selected_affine_extras_full_translation_v4_count"] == 0


def test_orientation_orbit_guardrail():
    result = audit.build_exact_v4_affine_mechanism_audit()
    orientation = result["orientation"]
    assert orientation["canonical_v4_square_symmetry_orbit_size"] >= 1
    assert orientation["exact_v4_terminal_sets_in_square_symmetry_orbit"] is True
    assert orientation["word_set_is_orientation_language"] is True
    assert orientation["affine_cell_value_criterion_is_stable_object"] is True


def test_affine_defect_separates_exact_v4_from_32_extras():
    result = audit.build_exact_v4_affine_mechanism_audit()
    defect = result["affine_defect"]
    assert defect["exact_v4_basis_mismatch_distribution"] == {"0": 144}
    assert defect["exact_v4_preserved_domain_affine_planes_distribution"] == {"140": 144}
    assert defect["exact_v4_preserved_permutation_diagonal_planes_distribution"] == {"24": 144}
    assert "0" not in defect["selected_affine_extra_basis_mismatch_distribution"]
    assert "140" not in defect["selected_affine_extra_preserved_domain_affine_planes_distribution"]
    assert "24" not in defect[
        "selected_affine_extra_preserved_permutation_diagonal_planes_distribution"
    ]
