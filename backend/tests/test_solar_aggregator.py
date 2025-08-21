import horary_engine.polarity_weights as polarity_weights
import horary_engine.dsl as dsl
from horary_engine.solar_aggregator import aggregate as solar_aggregate
from horary_engine.aggregator import aggregate as legacy_aggregate
from models import Planet, Aspect as AspectType
from rule_engine import get_rule_weight

role_importance = dsl.role_importance
Moon = dsl.Moon
L1 = dsl.L1
L10 = dsl.L10
LQ = dsl.LQ
aspect = dsl.aspect
translation = dsl.translation
reception = dsl.reception
collection = dsl.collection

TestimonyKey = polarity_weights.TestimonyKey
TOKEN_RULE_MAP = polarity_weights.TOKEN_RULE_MAP


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
    testimonies = [
        translation(Moon, L1, Planet.SUN, AspectType.SQUARE, True)
    ]
    contract = {"querent": Planet.MERCURY}
    score, ledger = solar_aggregate(testimonies, contract)
    token = TestimonyKey.TRANSLATION_SQUARE_WITH_RECEPTION
    expected = abs(get_rule_weight(TOKEN_RULE_MAP[token]))
    assert score == expected
    assert ledger[0]["key"] is token
    assert ledger[0]["applying"] is True


def test_dsl_collection_dispatch():
    testimonies = [collection(Moon, L1, Planet.SUN, AspectType.TRINE)]
    contract = {"querent": Planet.MERCURY}
    score, ledger = solar_aggregate(testimonies, contract)
    token = TestimonyKey.COLLECTION_TRINE_WITHOUT_RECEPTION
    expected = abs(get_rule_weight(TOKEN_RULE_MAP[token]))
    assert score == expected
    assert ledger[0]["key"] is token
    assert ledger[0]["applying"] is True


def test_dsl_reception_dispatch():
    testimonies = [reception(L10, L1, "mutual")]
    contract = {"querent": Planet.MERCURY, "l10": Planet.SUN}
    score, ledger = solar_aggregate(testimonies, contract)
    expected = abs(get_rule_weight(TOKEN_RULE_MAP[TestimonyKey.L10_FORTUNATE]))
    assert score == expected
    assert ledger[0]["key"] is TestimonyKey.L10_FORTUNATE


def test_generated_aspect_token_with_role_weights():
    contract = {"querent": Planet.MERCURY, "quesited": Planet.JUPITER, "quesited_house": 7}
    testimonies = [
        role_importance(L1, 0.5),
        role_importance(LQ, 0.5),
        aspect(L1, LQ, AspectType.TRINE),
    ]
    score, ledger = solar_aggregate(testimonies, contract)
    assert score == 0.0
    assert ledger[0]["key"] == "ASPECT_L1_TRINE_L7"
    assert ledger[0]["role_factor"] == 0.25
