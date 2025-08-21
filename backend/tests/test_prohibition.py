import sys
import json
import datetime
from pathlib import Path

import pytest
import swisseph as swe

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from models import Planet, PlanetPosition, Sign, HoraryChart, Aspect
from horary_engine.perfection import check_future_prohibitions
from horary_config import cfg


def _load_lottery_chart() -> HoraryChart:
    data_path = ROOT / "will I win the lottery.json"
    if not data_path.exists():
        pytest.skip("lottery chart file missing")
    with open(data_path, "r") as f:
        data = json.load(f)

    planets = {}
    for name, pd in data["planets"].items():
        planet_enum = Planet[name.upper()]
        sign_enum = Sign[pd["sign"].upper()]
        planets[planet_enum] = PlanetPosition(
            planet=planet_enum,
            longitude=pd["longitude"],
            latitude=pd["latitude"],
            house=pd["house"],
            sign=sign_enum,
            dignity_score=pd["dignity_score"],
            retrograde=pd["retrograde"],
            speed=pd["speed"],
        )

    dt_utc = datetime.datetime.fromisoformat(data["asked_at_utc"].replace("Z", "+00:00"))
    jd = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
    )

    return HoraryChart(
        date_time=dt_utc,
        date_time_utc=dt_utc,
        timezone_info=data["tz"],
        location=(data["location"]["lat"], data["location"]["lon"]),
        location_name=data["location"]["city"],
        planets=planets,
        aspects=[],
        houses=data["houses"],
        house_rulers={},
        ascendant=data["houses"][0],
        midheaven=data["houses"][9],
        julian_day=jd,
    )


def _calc_future_aspect_time(pos1, pos2, aspect, jd_start=None, max_days=None):
    target_angles = {
        Aspect.CONJUNCTION: 0,
        Aspect.SEXTILE: 60,
        Aspect.SQUARE: 90,
        Aspect.TRINE: 120,
        Aspect.OPPOSITION: 180,
    }
    target_angle = target_angles[aspect]
    relative_speed = pos1.speed - pos2.speed
    delta = (pos2.longitude + target_angle - pos1.longitude) % 360.0
    return delta / relative_speed


def test_venus_saturn_prohibits_future_sextile():
    chart = _load_lottery_chart()
    cfg().perfection.allow_out_of_sign = True

    t_main = _calc_future_aspect_time(
        chart.planets[Planet.VENUS],
        chart.planets[Planet.JUPITER],
        Aspect.SEXTILE,
    )
    assert t_main == pytest.approx(52.33, rel=0.01)

    result = check_future_prohibitions(
        chart, Planet.VENUS, Planet.JUPITER, t_main, _calc_future_aspect_time
    )
    assert result["prohibited"] is True
    assert result["prohibitor"] == Planet.SATURN
    assert result["significator"] == Planet.VENUS
    assert result["t_prohibition"] == pytest.approx(5.57, rel=0.05)


def test_translation_square_with_reception_positive_phrase():
    now = datetime.datetime.utcnow()
    planets = {
        Planet.VENUS: PlanetPosition(
            planet=Planet.VENUS,
            longitude=0.0,
            latitude=0.0,
            house=1,
            sign=Sign.ARIES,
            dignity_score=0,
            speed=1.0,
        ),
        Planet.JUPITER: PlanetPosition(
            planet=Planet.JUPITER,
            longitude=10.0,
            latitude=0.0,
            house=7,
            sign=Sign.SCORPIO,
            dignity_score=0,
            speed=1.0,
        ),
        Planet.MARS: PlanetPosition(
            planet=Planet.MARS,
            longitude=20.0,
            latitude=0.0,
            house=5,
            sign=Sign.CAPRICORN,
            dignity_score=0,
            speed=2.0,
        ),
        Planet.SUN: PlanetPosition(
            planet=Planet.SUN,
            longitude=50.0,
            latitude=0.0,
            house=10,
            sign=Sign.LEO,
            dignity_score=0,
            speed=1.0,
        ),
    }
    chart = HoraryChart(
        date_time=now,
        date_time_utc=now,
        timezone_info="UTC",
        location=(0.0, 0.0),
        location_name="Test",
        planets=planets,
        aspects=[],
        houses=[0.0] * 12,
        house_rulers={},
        ascendant=0.0,
        midheaven=0.0,
        julian_day=0.0,
    )

    cfg().perfection.require_in_sign = False

    def mock_calc(pos_a, pos_b, aspect, jd, max_days):
        if aspect == Aspect.SQUARE and pos_b.planet == Planet.MARS:
            return 2.0
        return None

    result = check_future_prohibitions(
        chart, Planet.VENUS, Planet.JUPITER, 10.0, mock_calc
    )

    assert result["type"] == "translation"
    assert result["translator"] == Planet.MARS
    assert result["aspect"] == Aspect.SQUARE
    assert result["quality"] == "with difficulty"
    assert result["reception"] is True
    assert (
        result["reason"]
        == "Perfection by translation (square): positive with difficulty (softened by reception)"
    )
