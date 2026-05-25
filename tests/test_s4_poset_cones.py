from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_s4_poset_cones.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_s4_poset_cones", SCRIPT)
posets = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(posets)


def test_labeled_poset_and_extension_set_counts():
    result = posets.build_s4_poset_cone_comparison()
    assert result["labeled_poset_count"] == 219
    assert result["unique_linear_extension_set_count"] > 0
    assert result["D4_or_V4_as_poset_cone"] == {"D4": False, "V4": False}


def test_poset_cone_tiler_distribution_is_stable():
    result = posets.build_s4_poset_cone_comparison()
    assert result["left_tiler_count"] > 0
    assert sum(result["left_tiler_size_distribution"].values()) == result["left_tiler_count"]
    assert all(int(size) in {1, 2, 3, 4, 6, 8, 12, 24} for size in result["left_tiler_size_distribution"])


def test_every_recorded_left_tiler_has_a_valid_tiling_size():
    result = posets.build_s4_poset_cone_comparison()
    for record in result["left_tilers"]:
        tiling = record["left_tiling"]["tiling"]
        assert len(tiling) == 24 // record["size"]
        covered = set()
        for tile in tiling:
            words = set(tile["words"])
            assert len(words) == record["size"]
            assert covered.isdisjoint(words)
            covered.update(words)
        assert len(covered) == 24
