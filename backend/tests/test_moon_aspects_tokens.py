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
from models import Planet, Aspect, PlanetPosition, HoraryChart, Sign, AspectInfo


def _make_pos(planet: Planet) -> PlanetPosition:
    return PlanetPosition(
        planet=planet,
        longitude=0.0,
        latitude=0.0,
        house=1,
        sign=Sign.ARIES,
        dignity_score=0,
        retrograde=False,
        speed=1.0,
    )


def _make_chart() -> HoraryChart:
    planets = {
        Planet.MOON: _make_pos(Planet.MOON),
        Planet.SUN: _make_pos(Planet.SUN),
        Planet.MERCURY: _make_pos(Planet.MERCURY),
    }
    aspects = [
        AspectInfo(Planet.MOON, Planet.SUN, Aspect.SEXTILE, 0.0, True),
        AspectInfo(Planet.MOON, Planet.MERCURY, Aspect.OPPOSITION, 0.0, True),
    ]
    dt = datetime.datetime(2024, 1, 1)
    return HoraryChart(
        date_time=dt,
        date_time_utc=dt,
        timezone_info="UTC",
        location=(0.0, 0.0),
        location_name="Test",
        planets=planets,
        aspects=aspects,
        houses=[0.0] * 12,
        house_rulers={},
        ascendant=0.0,
        midheaven=0.0,
    )


def test_new_tokens_scoring_and_rationale():
    tokens = [
        TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN,
        TestimonyKey.MOON_APPLYING_OPPOSITION_L1,
    ]
    score, ledger = aggregate(tokens)
    assert score == 0.0
    sextile_entry = next(e for e in ledger if e["key"] == TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN)
    assert sextile_entry["polarity"] is Polarity.POSITIVE
    assert sextile_entry["delta_yes"] == 1.0
    opposition_entry = next(e for e in ledger if e["key"] == TestimonyKey.MOON_APPLYING_OPPOSITION_L1)
    assert opposition_entry["polarity"] is Polarity.NEGATIVE
    assert opposition_entry["delta_no"] == 1.0
    rationale = build_rationale(ledger)
    assert f"{TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN.value} (+1.0)" in rationale
    assert f"{TestimonyKey.MOON_APPLYING_OPPOSITION_L1.value} (-1.0)" in rationale


def test_extract_testimonies_emits_tokens():
    chart = _make_chart()
    contract = {"examiner": Planet.SUN, "querent": Planet.MERCURY}
    primitives = extract_testimonies(chart, contract)
    assert TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN in primitives
    assert TestimonyKey.MOON_APPLYING_OPPOSITION_L1 in primitives
