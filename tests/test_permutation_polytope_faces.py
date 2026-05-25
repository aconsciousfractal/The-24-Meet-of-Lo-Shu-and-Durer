from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_permutation_polytope_faces.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_permutation_polytope_faces", SCRIPT)
faces = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(faces)


def test_v4_is_not_a_face_of_d4_permutation_polytope():
    result = faces.build_permutation_polytope_face_audit()
    assert result["face_tests"]["P_V4_is_face_of_P_D4"]["is_face"] is False
    assert result["conclusion"]["P_V4_is_face_of_P_D4"] is False


def test_d4_and_v4_are_not_birkhoff_faces():
    result = faces.build_permutation_polytope_face_audit()
    d4 = result["face_tests"]["P_D4_is_birkhoff_face_by_support"]
    v4 = result["face_tests"]["P_V4_is_birkhoff_face_by_support"]
    assert d4["support_size"] == 16
    assert v4["support_size"] == 16
    assert d4["birkhoff_face_completion_size"] == 24
    assert v4["birkhoff_face_completion_size"] == 24
    assert d4["is_birkhoff_face_vertex_set"] is False
    assert v4["is_birkhoff_face_vertex_set"] is False


def test_d4_and_v4_f_vectors_are_stable():
    result = faces.build_permutation_polytope_face_audit()
    assert result["f_vectors"]["P_D4"]["polytope_dimension"] == 5
    assert result["f_vectors"]["P_D4"]["f_vector"] == {
        "0": 8,
        "1": 24,
        "2": 34,
        "3": 24,
        "4": 8,
    }
    assert result["f_vectors"]["P_V4"]["polytope_dimension"] == 3
    assert result["f_vectors"]["P_V4"]["f_vector"] == {
        "0": 4,
        "1": 6,
        "2": 4,
    }


def test_v4_faces_are_tetrahedral():
    result = faces.build_permutation_polytope_face_audit()
    v4_faces = result["f_vectors"]["P_V4"]["faces_by_dimension"]
    assert len(v4_faces["0"]) == 4
    assert len(v4_faces["1"]) == 6
    assert len(v4_faces["2"]) == 4
