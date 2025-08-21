from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from horary_engine.polarity_weights import TestimonyKey, TOKEN_RULE_MAP
from horary_engine.aggregator import aggregate
from rule_engine import get_rule_weight


@pytest.mark.parametrize("token, rule_id", TOKEN_RULE_MAP.items())
def test_token_weight_alignment(token: TestimonyKey, rule_id: str):
    score, ledger = aggregate([token])
    expected = get_rule_weight(rule_id)
    assert score == expected
    if expected >= 0:
        assert ledger[0]["delta_yes"] == abs(expected)
    else:
        assert ledger[0]["delta_no"] == abs(expected)
