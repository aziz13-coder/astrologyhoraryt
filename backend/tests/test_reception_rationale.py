import datetime
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from horary_engine.engine import extract_testimonies
from horary_engine.solar_aggregator import aggregate
from horary_engine.rationale import build_rationale
from models import Planet, PlanetPosition, HoraryChart, Sign


def _make_pos(planet: Planet, sign: Sign) -> PlanetPosition:
    return PlanetPosition(
        planet=planet,
        longitude=sign.start_degree,
        latitude=0.0,
        house=1,
        sign=sign,
        dignity_score=0,
        retrograde=False,
        speed=1.0,
    )


def _make_chart() -> HoraryChart:
    planets = {
        Planet.MARS: _make_pos(Planet.MARS, Sign.TAURUS),
        Planet.VENUS: _make_pos(Planet.VENUS, Sign.ARIES),
        Planet.SUN: _make_pos(Planet.SUN, Sign.CANCER),
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
        houses=[i * 30.0 for i in range(12)],
        house_rulers={},
        ascendant=0.0,
        midheaven=0.0,
    )


def test_mutual_reception_rationale():
    chart = _make_chart()
    contract = {"querent": Planet.MARS, "quesited": Planet.VENUS}
    primitives = extract_testimonies(chart, contract)
    score, ledger = aggregate(primitives, contract)
    rationale = build_rationale(ledger)
    assert any("Mars receives Venus" in line for line in rationale)
    assert any("Venus receives Mars" in line for line in rationale)

