import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from horary_engine.polarity_weights import TestimonyKey
from horary_engine.aggregator import aggregate
from horary_engine.rationale import build_rationale
from horary_engine.polarity import Polarity
from horary_engine.engine import extract_testimonies
from models import Planet, PlanetPosition, HoraryChart, Sign


def _make_pos(planet: Planet, dignity: int = 0) -> PlanetPosition:
    return PlanetPosition(
        planet=planet,
        longitude=0.0,
        latitude=0.0,
        house=1,
        sign=Sign.ARIES,
        dignity_score=dignity,
        retrograde=False,
        speed=1.0,
    )


def _chart_one() -> HoraryChart:
    planets = {
        Planet.VENUS: _make_pos(Planet.VENUS, dignity=5),
        Planet.MARS: _make_pos(Planet.MARS, dignity=0),
        Planet.JUPITER: _make_pos(Planet.JUPITER, dignity=5),
        Planet.SATURN: _make_pos(Planet.SATURN, dignity=-5),
    }
    dt = datetime.datetime(2024, 1, 1)
    return HoraryChart(
        date_time=dt,
        date_time_utc=dt,
        timezone_info="UTC",
        location=(0.0, 0.0),
        location_name="Test",
        planets=planets,
        aspects=[],
        houses=[0.0] * 12,
        house_rulers={7: Planet.VENUS, 2: Planet.MARS, 5: Planet.JUPITER, 8: Planet.SATURN},
        ascendant=0.0,
        midheaven=0.0,
    )


def _chart_two() -> HoraryChart:
    planets = {
        Planet.SATURN: _make_pos(Planet.SATURN, dignity=-5),
        Planet.VENUS: _make_pos(Planet.VENUS, dignity=5),
        Planet.JUPITER: _make_pos(Planet.JUPITER, dignity=5),
        Planet.MARS: _make_pos(Planet.MARS, dignity=0),
    }
    dt = datetime.datetime(2024, 1, 1)
    return HoraryChart(
        date_time=dt,
        date_time_utc=dt,
        timezone_info="UTC",
        location=(0.0, 0.0),
        location_name="Test",
        planets=planets,
        aspects=[],
        houses=[0.0] * 12,
        house_rulers={7: Planet.SATURN, 2: Planet.VENUS, 5: Planet.SATURN, 8: Planet.JUPITER},
        ascendant=0.0,
        midheaven=0.0,
    )


def test_category_tokens_scoring_and_rationale():
    for token, polarity in [
        (TestimonyKey.L7_FORTUNATE, Polarity.POSITIVE),
        (TestimonyKey.L7_MALIFIC_DEBILITY, Polarity.NEGATIVE),
        (TestimonyKey.L2_FORTUNATE, Polarity.POSITIVE),
        (TestimonyKey.L2_MALIFIC_DEBILITY, Polarity.NEGATIVE),
        (TestimonyKey.L8_FORTUNATE, Polarity.POSITIVE),
        (TestimonyKey.L8_MALIFIC_DEBILITY, Polarity.NEGATIVE),
        (TestimonyKey.L5_FORTUNATE, Polarity.POSITIVE),
        (TestimonyKey.L5_MALIFIC_DEBILITY, Polarity.NEGATIVE),
    ]:
        score, ledger = aggregate([token])
        entry = ledger[0]
        assert entry["polarity"] is polarity
        if polarity is Polarity.POSITIVE:
            assert entry["delta_yes"] == 1.0
        else:
            assert entry["delta_no"] == 1.0
        rationale = build_rationale(ledger)
        sign = "+" if polarity is Polarity.POSITIVE else "-"
        assert f"{token.value} ({sign}1.0)" in rationale


def test_extract_testimonies_emits_category_tokens():
    chart = _chart_one()
    primitives = extract_testimonies(chart, {})
    assert TestimonyKey.L7_FORTUNATE in primitives
    assert TestimonyKey.L2_MALIFIC_DEBILITY in primitives
    assert TestimonyKey.L5_FORTUNATE in primitives
    assert TestimonyKey.L8_MALIFIC_DEBILITY in primitives


def test_extract_testimonies_emits_inverse_tokens():
    chart = _chart_two()
    primitives = extract_testimonies(chart, {})
    assert TestimonyKey.L7_MALIFIC_DEBILITY in primitives
    assert TestimonyKey.L2_FORTUNATE in primitives
    assert TestimonyKey.L5_MALIFIC_DEBILITY in primitives
    assert TestimonyKey.L8_FORTUNATE in primitives
