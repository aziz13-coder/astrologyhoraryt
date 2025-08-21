import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from evaluate_chart import evaluate_chart
from horary_engine.engine import EnhancedTraditionalHoraryJudgmentEngine
from horary_engine.serialization import serialize_chart_for_frontend


def test_evaluate_chart_handles_serialized_chart_data():
    engine = EnhancedTraditionalHoraryJudgmentEngine()
    dt_local = datetime.datetime(2024, 1, 1, 12, 0, 0)
    dt_utc = dt_local
    chart = engine.calculator.calculate_chart(dt_local, dt_utc, "UTC", 51.5, -0.1, "Test")
    chart_data = serialize_chart_for_frontend(chart, chart.solar_analyses)
    result = evaluate_chart(chart_data)
    assert isinstance(result.get("ledger"), list)
