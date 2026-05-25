from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_affine_normal_count_derivation.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location(
    "analyze_affine_normal_count_derivation", SCRIPT
)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_balanced_direction_count():
    result = audit.build_affine_normal_count_derivation()
    assert result["two_dimensional_subspace_count"] == 35
    assert result["balanced_direction_count"] == 13
    assert result["domain_magic_directions_pairwise_complementary"]


def test_good_linear_part_count():
    result = audit.build_affine_normal_count_derivation()
    assert result["gl4_linear_part_count"] == 20160
    assert result["ordered_pairwise_complementary_balanced_triple_count"] == 36
    assert result["balanced_complementarity_graph"] == {
        "vertex_count": 13,
        "edge_count": 27,
        "triangle_count": 6,
        "ordered_triangle_count": 36,
    }
    assert result["domain_triple_stabilizer_size"] == 6
    assert result["good_linear_part_count"] == 216
    assert result["image_triple_count"] == 36
    assert result["image_triple_multiplicity_distribution"] == {"6": 36}


def test_admissible_masks_are_square_symmetry_torsor():
    result = audit.build_affine_normal_count_derivation()
    assert result["admissible_mask_torsor"] == {
        "admissible_mask_count": 8,
        "square_symmetry_count": 8,
        "orbit_count": 1,
        "orbit_size_distribution": {"8": 8},
        "stabilizer_size_distribution": {"1": 8},
        "is_free_transitive": True,
    }


def test_essential_affine_representative_count_derivation():
    result = audit.build_affine_normal_count_derivation()
    assert result["offset_count"] == 16
    assert result["raw_affine_magic_square_count"] == 3456
    assert result["square_symmetry_orbit_size_for_normal_squares"] == 8
    assert result["essential_affine_representative_count"] == 432
