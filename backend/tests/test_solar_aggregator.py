from pathlib import Path
import sys
import types
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = ROOT / "backend" / "horary_engine"
sys.path.append(str(ROOT / "backend"))

# Create lightweight package to avoid heavy initialization
pkg = types.ModuleType("horary_engine")
pkg.__path__ = [str(MODULE_DIR)]
sys.modules["horary_engine"] = pkg


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        f"horary_engine.{name}", MODULE_DIR / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"horary_engine.{name}"] = module
    spec.loader.exec_module(module)
    return module


polarity_weights = _load("polarity_weights")
dsl = _load("dsl")
_load("dsl_to_testimony")
solar_aggregator_module = _load("solar_aggregator")
aggregator_module = _load("aggregator")

role_importance = dsl.role_importance
Moon = dsl.Moon
L1 = dsl.L1
L10 = dsl.L10
aspect = dsl.aspect
translation = dsl.translation
reception = dsl.reception

from models import Planet, Aspect as AspectType
from rule_engine import get_rule_weight

TestimonyKey = polarity_weights.TestimonyKey
TOKEN_RULE_MAP = polarity_weights.TOKEN_RULE_MAP
solar_aggregate = solar_aggregator_module.aggregate
legacy_aggregate = aggregator_module.aggregate


def test_role_importance_scales_weights():
    testimonies = [
        role_importance(Moon, 0.7),
        TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN,
    ]
    score, ledger = solar_aggregate(testimonies)
    base = abs(
        get_rule_weight(TOKEN_RULE_MAP[TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN])
    )
    expected = base * 0.7
    assert score == expected
    assert ledger[0]["weight"] == expected


def test_legacy_and_solar_equal_without_importance():
    tokens = [TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN]
    score_legacy, _ = legacy_aggregate(tokens)
    score_solar, _ = solar_aggregate(tokens)
    assert score_legacy == score_solar


def test_solar_scales_relative_to_legacy():
    tokens = [TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN]
    score_legacy, _ = legacy_aggregate(tokens)
    score_solar, _ = solar_aggregate(
        [role_importance(Moon, 0.5), TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN]
    )
    assert score_solar == score_legacy * 0.5


def test_role_matching_uses_delimiters():
    testimonies = [
        role_importance(L1, 0.5),
        role_importance(L10, 2.0),
        TestimonyKey.L10_FORTUNATE,
    ]
    score, ledger = solar_aggregate(testimonies)
    assert score == 2.0
    assert ledger[0]["weight"] == 2.0


def test_dsl_aspect_dispatch():
    testimonies = [aspect(Moon, Planet.SUN, AspectType.TRINE)]
    score, ledger = solar_aggregate(testimonies)
    expected = abs(
        get_rule_weight(
            TOKEN_RULE_MAP[TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN]
        )
    )
    assert score == expected
    assert ledger[0]["key"] is TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN


def test_dsl_translation_dispatch():
    testimonies = [translation(Moon, L1, Planet.SUN)]
    score, ledger = solar_aggregate(testimonies)
    expected = abs(
        get_rule_weight(
            TOKEN_RULE_MAP[TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT]
        )
    )
    assert score == expected
    assert ledger[0]["key"] is TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT


def test_dsl_reception_dispatch():
    testimonies = [reception(L10, L1, "mutual")]
    score, ledger = solar_aggregate(testimonies)
    expected = abs(get_rule_weight(TOKEN_RULE_MAP[TestimonyKey.L10_FORTUNATE]))
    assert score == expected
    assert ledger[0]["key"] is TestimonyKey.L10_FORTUNATE
