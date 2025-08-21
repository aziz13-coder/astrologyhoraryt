from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

import evaluate_chart
from horary_engine.polarity_weights import TestimonyKey


class DummyConfig:
    def __init__(self, data):
        self.data = data

    def get(self, key, default=None):
        value = self.data
        for part in key.split('.'):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        return value


def test_evaluate_chart_applies_custom_role_importance(monkeypatch):
    cfg_data = {
        "aggregator": {
            "use_dsl": True,
            "role_importance": {
                "L1": 1.0,
                "LQ": 1.0,
                "Moon": 0.7,
                "L10": 2.0,
                "L3": 1.0,
            },
        }
    }
    monkeypatch.setattr(evaluate_chart, "cfg", lambda: DummyConfig(cfg_data))
    monkeypatch.setattr(evaluate_chart, "get_contract", lambda category: {})
    monkeypatch.setattr(
        evaluate_chart, "extract_testimonies", lambda chart, contract: [TestimonyKey.L10_FORTUNATE]
    )

    result = evaluate_chart.evaluate_chart({}, use_dsl=None)
    ledger = result["ledger"]
    assert ledger[0]["weight"] == 2.0
    assert ledger[0]["role_factor"] == 2.0
