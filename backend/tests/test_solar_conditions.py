from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from models import Planet, PlanetPosition, Sign, SolarCondition
from horary_engine.engine import EnhancedTraditionalAstrologicalCalculator

def make_position(planet, lon):
    return PlanetPosition(
        planet=planet,
        longitude=lon,
        latitude=0.0,
        house=1,
        sign=Sign.ARIES,
        dignity_score=0,
    )

def analyze(planet, lon, engine=None):
    if engine is None:
        engine = EnhancedTraditionalAstrologicalCalculator()
    sun_pos = make_position(Planet.SUN, 0.0)
    planet_pos = make_position(planet, lon)
    return engine._analyze_enhanced_solar_condition(
        planet, planet_pos, sun_pos, 0.0, 0.0, 0.0
    )

def test_fixed_boundaries_classification():
    engine = EnhancedTraditionalAstrologicalCalculator()
    assert analyze(Planet.MOON, 0.2, engine).condition == SolarCondition.CAZIMI
    assert analyze(Planet.MOON, 5.0, engine).condition == SolarCondition.COMBUSTION
    assert analyze(Planet.MOON, 9.0, engine).condition == SolarCondition.UNDER_BEAMS
    assert analyze(Planet.MOON, 20.0, engine).condition == SolarCondition.FREE

def test_visibility_exception_flagged(monkeypatch):
    engine = EnhancedTraditionalAstrologicalCalculator()
    monkeypatch.setattr(
        engine,
        "_check_enhanced_combustion_exception",
        lambda *args, **kwargs: True,
    )
    analysis = analyze(Planet.MERCURY, 9.0, engine)
    assert analysis.condition == SolarCondition.UNDER_BEAMS
    assert analysis.traditional_exception is True


def test_scoring_and_textual_flag(monkeypatch):
    engine = EnhancedTraditionalAstrologicalCalculator()
    houses = [i * 30.0 for i in range(12)]
    sun_pos = make_position(Planet.SUN, 0.0)

    # Under beams without exception
    planet_pos = make_position(Planet.MOON, 9.0)
    analysis = engine._analyze_enhanced_solar_condition(
        Planet.MOON, planet_pos, sun_pos, 0.0, 0.0, 0.0
    )
    res = engine._calculate_comprehensive_traditional_dignity(
        Planet.MOON, planet_pos, houses, sun_pos, analysis
    )
    assert "under_beams" in res["dignities"]
    penalized_score = res["score"]

    # Under beams with visibility exception
    planet_pos2 = make_position(Planet.MERCURY, 9.0)
    monkeypatch.setattr(
        engine,
        "_check_enhanced_combustion_exception",
        lambda *args, **kwargs: True,
    )
    analysis2 = engine._analyze_enhanced_solar_condition(
        Planet.MERCURY, planet_pos2, sun_pos, 0.0, 0.0, 0.0
    )
    res2 = engine._calculate_comprehensive_traditional_dignity(
        Planet.MERCURY, planet_pos2, houses, sun_pos, analysis2
    )
    assert analysis2.traditional_exception is True
    assert "under_beams" in res2["dignities"]
    assert res2["score"] > penalized_score
