from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
SCRIPT = SCRIPT_DIR / "analyze_terminal24_markov_graph.py"

sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("analyze_terminal24_markov_graph", SCRIPT)
markov = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(markov)


def test_pm1_kernel_move_count_and_support_distribution():
    result = markov.build_terminal24_markov_graph()
    assert result["move_count_up_to_sign"] == 109
    assert result["signed_move_count"] == 218
    assert result["move_support_distribution_up_to_sign"] == {
        "4": 2,
        "6": 24,
        "8": 47,
        "10": 16,
        "12": 12,
        "16": 8,
    }


def test_terminal24_markov_graph_size_and_components():
    result = markov.build_terminal24_markov_graph()
    assert result["node_count"] == 236
    assert result["edge_count"] == 247
    assert result["component_count"] == 98
    assert result["component_size_distribution"] == {
        "1": 50,
        "2": 13,
        "4": 28,
        "6": 4,
        "8": 3,
    }


def test_terminal24_markov_graph_degree_distribution():
    result = markov.build_terminal24_markov_graph()
    assert result["degree_distribution"] == {
        "0": 50,
        "1": 36,
        "2": 8,
        "3": 130,
        "4": 10,
        "6": 2,
    }
    assert result["class_degree_distributions"]["main_extra"] == {"0": 12, "1": 20}
    assert result["class_degree_distributions"]["outside_main"] == {"0": 38, "1": 14, "2": 8}


def test_terminal24_markov_graph_edge_class_counts():
    result = markov.build_terminal24_markov_graph()
    assert result["edge_class_counts"] == {
        "('exact_v4', 'exact_v4')": 218,
        "('exact_v4', 'outside_main')": 8,
        "('main_extra', 'main_extra')": 3,
        "('main_extra', 'outside_main')": 14,
        "('outside_main', 'outside_main')": 4,
    }


def test_terminal24_markov_graph_component_class_profiles():
    result = markov.build_terminal24_markov_graph()
    assert result["component_class_profiles"] == {
        "exact_v4:4": 28,
        "exact_v4:4,main_extra:2,outside_main:2": 2,
        "exact_v4:4,outside_main:2": 4,
        "exact_v4:8": 1,
        "main_extra:1": 12,
        "main_extra:1,outside_main:1": 10,
        "main_extra:2": 3,
        "outside_main:1": 38,
    }
