from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

try:
    from ..horary_engine.aspects import calculate_moon_next_aspect
except ImportError:  # pragma: no cover - fallback for direct execution
    from horary_engine.aspects import calculate_moon_next_aspect

try:
    from ..models import Planet, PlanetPosition, Sign
except ImportError:  # pragma: no cover - fallback for direct execution
    from models import Planet, PlanetPosition, Sign

from horary_engine.calculation import is_within_sign_change
from horary_engine.dsl import accidental
from horary_engine.solar_aggregator import aggregate as solar_aggregate
from horary_engine.polarity_weights import TestimonyKey, TOKEN_RULE_MAP
from rule_engine import get_rule_weight


def test_cross_sign_perfection_disallowed():
    planets = {
        Planet.MOON: PlanetPosition(
            planet=Planet.MOON,
            longitude=29.0,
            latitude=0.0,
            house=1,
            sign=Sign.ARIES,
            dignity_score=0,
            speed=13.0,
        ),
        Planet.SUN: PlanetPosition(
            planet=Planet.SUN,
            longitude=31.0,
            latitude=0.0,
            house=1,
            sign=Sign.TAURUS,
            dignity_score=0,
            speed=1.0,
        ),
    }

    aspect = calculate_moon_next_aspect(planets, jd_ut=0.0, get_moon_speed=lambda _: 13.0)
    assert aspect is None


def test_ignores_non_classical_targets():
    planets = {
        Planet.MOON: PlanetPosition(
            planet=Planet.MOON,
            longitude=18.0,
            latitude=0.0,
            house=1,
            sign=Sign.ARIES,
            dignity_score=0,
            speed=13.0,
        ),
        Planet.ASC: PlanetPosition(
            planet=Planet.ASC,
            longitude=80.0,
            latitude=0.0,
            house=1,
            sign=Sign.GEMINI,
            dignity_score=0,
            speed=0.0,
        ),
    }

    aspect = calculate_moon_next_aspect(planets, jd_ut=0.0, get_moon_speed=lambda _: 13.0)
    assert aspect is None


def test_sign_change_detection_positive():
    assert is_within_sign_change(29.5, 1.0, threshold=2.0)


def test_sign_change_detection_negative():
    assert not is_within_sign_change(15.0, 1.0, threshold=2.0)


def test_sign_change_token_dispatch():
    score, ledger = solar_aggregate([accidental(Planet.SUN, "sign_change")])
    expected = get_rule_weight(TOKEN_RULE_MAP[TestimonyKey.SIGN_CHANGE_SUN])
    assert score == expected
    assert ledger[0]["key"] == TestimonyKey.SIGN_CHANGE_SUN
    assert ledger[0]["delta_no"] == abs(expected)

