import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from rule_engine import evaluate_rules, get_rule_weight


def test_perfection_rule_moon_applying_mercury():
    assert evaluate_rules(["P4"]) == ["P4"]
    assert get_rule_weight("P4") == 1.5


def test_special_topic_mutual_reception_l7_mercury():
    assert evaluate_rules(["S3"]) == ["S3"]
    assert get_rule_weight("S3") == 1.5


def test_special_topic_l7_sign_change():
    assert evaluate_rules(["S4"]) == ["S4"]
    assert get_rule_weight("S4") == 1.2


def test_special_topic_priority():
    # When both special topic rules fire, lowest ID wins
    assert evaluate_rules(["S3", "S4"]) == ["S3"]
