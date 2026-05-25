import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "forbidden_shadow_split_p6.json"
SCRIPT = ROOT / "scripts" / "analyze_forbidden_shadow_split_p6.py"


def load_result():
    if not RESULT.exists():
        subprocess.run([sys.executable, str(SCRIPT), "--write"], check=True)
    return json.loads(RESULT.read_text())


def test_p6_quotient_shadow_lemma_payload():
    result = load_result()
    lemma = result["quotient_shadow_lemma"]
    assert lemma["spread_dimension"] == 2
    assert lemma["plane_dimension"] == 2
    assert lemma["possible_quotient_image_dimensions"] == [0, 1, 2]
    assert lemma["allowed_sorted_shadows"] == [
        "4,0,0,0",
        "2,2,0,0",
        "1,1,1,1",
    ]
    assert lemma["forbidden_shadow"] == "2,1,1,0"


def test_p6_extra32_f2110_split_is_terminal_set_split():
    result = load_result()
    assert result["extra32_count"] == 32
    assert result["F_2110_distribution"] == {"12": 16, "16": 16}
    assert result["F_2110_by_terminal_set_class"] == {
        "12": {"two_diagonal_pair": 16},
        "16": {"v4_like_0213": 8, "v4_like_1302": 8},
    }
    assert result["F_2110_by_translation_subset"] == {
        "12": {"True": 16},
        "16": {"False": 16},
    }
    assert result["equivalences"] == {
        "F_2110_12_iff_terminal_translation_subset": True,
        "F_2110_12_iff_two_diagonal_pair": True,
        "F_2110_16_iff_v4_like": True,
    }


def test_p6_terminal_profile_rows():
    result = load_result()
    rows = result["terminal_profile_rows"]
    assert len(rows) == 3
    counts = {
        (
            row["profile"]["terminal_set_class"],
            row["profile"]["F_2110"],
            tuple(row["profile"]["terminal_diagonal_set"]),
        ): row["count"]
        for row in rows
    }
    assert counts == {
        ("two_diagonal_pair", 12, ("0123", "3210")): 16,
        ("v4_like_0213", 16, ("0123", "0213", "3120", "3210")): 8,
        ("v4_like_1302", 16, ("0123", "1302", "2031", "3210")): 8,
    }
