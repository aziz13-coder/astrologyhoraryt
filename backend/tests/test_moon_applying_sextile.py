import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

try:
    from ..horary_engine.aspects import (
        calculate_enhanced_aspects,
        calculate_moon_next_aspect,
    )
except ImportError:  # pragma: no cover
    from horary_engine.aspects import (
        calculate_enhanced_aspects,
        calculate_moon_next_aspect,
    )

try:
    from ..models import Aspect, Planet, PlanetPosition, Sign
except ImportError:  # pragma: no cover
    from models import Aspect, Planet, PlanetPosition, Sign


def test_moon_sextile_mars_applying_consistency():
    planets = {
        Planet.MOON: PlanetPosition(
            planet=Planet.MOON,
            longitude=69.2,
            latitude=0.0,
            house=1,
            sign=Sign.GEMINI,
            dignity_score=0,
            speed=13.0,
        ),
        Planet.MARS: PlanetPosition(
            planet=Planet.MARS,
            longitude=10.0,
            latitude=0.0,
            house=1,
            sign=Sign.ARIES,
            dignity_score=0,
            speed=0.7,
        ),
    }

    jd_ut = 0.0

    # Enhanced aspects API
    aspects = calculate_enhanced_aspects(planets, jd_ut)
    moon_mars = next(
        a for a in aspects if {a.planet1, a.planet2} == {Planet.MOON, Planet.MARS}
    )
    assert moon_mars.aspect == Aspect.SEXTILE
    assert moon_mars.applying

    # Moon considerations API
    moon_next = calculate_moon_next_aspect(
        planets, jd_ut, get_moon_speed=lambda _: 13.0
    )
    assert moon_next is not None
    assert moon_next.planet == Planet.MARS
    assert moon_next.aspect == Aspect.SEXTILE
    assert moon_next.applying
