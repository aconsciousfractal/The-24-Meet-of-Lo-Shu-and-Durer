from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_kernel_v4_o5.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_kernel_v4_o5", SCRIPT)
audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def test_direct_kernel_identification_fails_uniformly():
    result = audit.build_kernel_v4_o5()
    assert result["terminal24_affine_record_count"] == 144
    assert result["value_bit_kernel_size"] == 4
    assert result["selected_plane_kernel_stabilizer_size_distribution"] == {
        "2": 144
    }
    assert result["selected_plane_kernel_orbit_size_distribution"] == {"2": 144}
    assert result["kernel_orbit_intersection_with_terminal_planes_distribution"] == {
        "0": 144
    }
    assert result["kernel_orbit_equals_terminal_translation_image_planes"] == {
        "False": 144
    }
    assert result["interpretation"]["direct_kernel_identification"] == "false"


def test_terminal_translation_v4_has_uniform_parallel_class_image():
    result = audit.build_kernel_v4_o5()
    assert result["terminal_set_full_translation_v4_distribution"] == {"True": 144}
    assert result["terminal_translation_image_plane_count_distribution"] == {
        "4": 144
    }
    assert result["terminal_translation_image_direction_count_distribution"] == {
        "1": 144
    }
    assert result["terminal_translation_image_direction_balanced_distribution"] == {
        "True": 144
    }
    assert result["terminal_plane_selected_intersection_pattern_distribution"] == {
        "(1, 1, 1, 1)": 144
    }
    assert set(result["terminal_translation_image_direction_distribution"].values()) == {
        24
    }
    assert len(result["terminal_translation_image_direction_distribution"]) == 6
