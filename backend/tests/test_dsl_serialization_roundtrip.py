import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

from horary_engine.dsl import (
    aspect,
    translation,
    collection,
    prohibition,
    refranation,
    frustration,
    abscission,
    reception,
    essential,
    accidental,
    moon_voc,
    house,
    role_importance,
    L1,
    LQ,
)
from models import Planet, Aspect as AspectType
from horary_engine.serialization import serialize_primitive, deserialize_primitive

PRIMITIVES = [
    aspect(Planet.SUN, Planet.MOON, AspectType.TRINE),
    translation(
        Planet.MERCURY,
        Planet.MARS,
        Planet.VENUS,
        AspectType.SEXTILE,
        True,
    ),
    collection(Planet.JUPITER, L1, LQ, AspectType.CONJUNCTION, True),
    prohibition(Planet.SATURN, L1, AspectType.SQUARE),
    refranation(Planet.MARS, L1),
    frustration(Planet.VENUS, L1, LQ),
    abscission(Planet.JUPITER, Planet.MARS, Planet.SATURN),
    reception(Planet.SUN, Planet.MOON, "exalt"),
    essential(Planet.MARS, 5),
    accidental(Planet.VENUS, "retro"),
    moon_voc(True, "test"),
    house(Planet.MERCURY, 3),
    role_importance(L1, 1.2),
]


@pytest.mark.parametrize("primitive", PRIMITIVES)
def test_round_trip_serialization(primitive):
    data = serialize_primitive(primitive)
    restored = deserialize_primitive(data)
    assert restored == primitive
