"""Central repository for testimony polarity and weight tables."""

from __future__ import annotations

from enum import Enum

from .polarity import Polarity
try:
    from ..rule_engine import get_rule_weight
except ImportError:  # pragma: no cover - fallback when executed as script
    from rule_engine import get_rule_weight


class TestimonyKey(Enum):
    """Canonical keys for all supported testimony tokens."""

    MOON_APPLYING_TRINE_EXAMINER_SUN = "moon_applying_trine_examiner_sun"
    MOON_APPLYING_SQUARE_EXAMINER_SUN = "moon_applying_square_examiner_sun"
    MOON_APPLYING_SEXTILE_EXAMINER_SUN = "moon_applying_sextile_examiner_sun"
    MOON_APPLYING_SEXTILE_L1 = "moon_applying_sextile_l1"
    MOON_APPLYING_SEXTILE_L7 = "moon_applying_sextile_l7"
    MOON_APPLYING_OPPOSITION_EXAMINER_SUN = "moon_applying_opposition_examiner_sun"
    MOON_APPLYING_OPPOSITION_L1 = "moon_applying_opposition_l1"
    MOON_APPLYING_OPPOSITION_L7 = "moon_applying_opposition_l7"
    L10_FORTUNATE = "l10_fortunate"
    L7_FORTUNATE = "l7_fortunate"
    L7_MALIFIC_DEBILITY = "l7_malific_debility"
    L2_FORTUNATE = "l2_fortunate"
    L2_MALIFIC_DEBILITY = "l2_malific_debility"
    L8_FORTUNATE = "l8_fortunate"
    L8_MALIFIC_DEBILITY = "l8_malific_debility"
    L5_FORTUNATE = "l5_fortunate"
    L5_MALIFIC_DEBILITY = "l5_malific_debility"
    PERFECTION_DIRECT = "perfection_direct"
    PERFECTION_TRANSLATION_OF_LIGHT = "perfection_translation_of_light"
    PERFECTION_COLLECTION_OF_LIGHT = "perfection_collection_of_light"
    ESSENTIAL_DETRIMENT = "essential_detriment"
    ACCIDENTAL_RETROGRADE = "accidental_retrograde"


# Prevent pytest from collecting the enum as a test class
TestimonyKey.__test__ = False


POLARITY_TABLE: dict[TestimonyKey, Polarity] = {
    # Favorable Moon applying trine to the examiner (Sun in education questions)
    TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN: Polarity.POSITIVE,
    # Example negative testimony
    TestimonyKey.MOON_APPLYING_SQUARE_EXAMINER_SUN: Polarity.NEGATIVE,
    # Moon applying sextile aspects (positive)
    TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN: Polarity.POSITIVE,
    TestimonyKey.MOON_APPLYING_SEXTILE_L1: Polarity.POSITIVE,
    TestimonyKey.MOON_APPLYING_SEXTILE_L7: Polarity.POSITIVE,
    # Moon applying opposition aspects (negative)
    TestimonyKey.MOON_APPLYING_OPPOSITION_EXAMINER_SUN: Polarity.NEGATIVE,
    TestimonyKey.MOON_APPLYING_OPPOSITION_L1: Polarity.NEGATIVE,
    TestimonyKey.MOON_APPLYING_OPPOSITION_L7: Polarity.NEGATIVE,
    # Fortunate outcome promised by L10
    TestimonyKey.L10_FORTUNATE: Polarity.POSITIVE,
    TestimonyKey.L7_FORTUNATE: Polarity.POSITIVE,
    TestimonyKey.L7_MALIFIC_DEBILITY: Polarity.NEGATIVE,
    TestimonyKey.L2_FORTUNATE: Polarity.POSITIVE,
    TestimonyKey.L2_MALIFIC_DEBILITY: Polarity.NEGATIVE,
    TestimonyKey.L8_FORTUNATE: Polarity.POSITIVE,
    TestimonyKey.L8_MALIFIC_DEBILITY: Polarity.NEGATIVE,
    TestimonyKey.L5_FORTUNATE: Polarity.POSITIVE,
    TestimonyKey.L5_MALIFIC_DEBILITY: Polarity.NEGATIVE,
    # Perfection testimonies are positive by default
    TestimonyKey.PERFECTION_DIRECT: Polarity.POSITIVE,
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: Polarity.POSITIVE,
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: Polarity.POSITIVE,
    # Debility indicators
    TestimonyKey.ESSENTIAL_DETRIMENT: Polarity.NEGATIVE,
    TestimonyKey.ACCIDENTAL_RETROGRADE: Polarity.NEGATIVE,
}

# Mapping of tokens to rule identifiers for dynamic weight resolution
TOKEN_RULE_MAP: dict[TestimonyKey, str] = {
    TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN: "M1",
    TestimonyKey.MOON_APPLYING_SQUARE_EXAMINER_SUN: "M3",
    TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN: "M4",
    TestimonyKey.MOON_APPLYING_SEXTILE_L1: "M5",
    TestimonyKey.MOON_APPLYING_SEXTILE_L7: "M6",
    TestimonyKey.MOON_APPLYING_OPPOSITION_EXAMINER_SUN: "M7",
    TestimonyKey.MOON_APPLYING_OPPOSITION_L1: "M8",
    TestimonyKey.MOON_APPLYING_OPPOSITION_L7: "M9",
    TestimonyKey.L10_FORTUNATE: "LC1",
    TestimonyKey.L7_FORTUNATE: "LC2",
    TestimonyKey.L7_MALIFIC_DEBILITY: "LC3",
    TestimonyKey.L2_FORTUNATE: "LC4",
    TestimonyKey.L2_MALIFIC_DEBILITY: "LC5",
    TestimonyKey.L8_FORTUNATE: "LC6",
    TestimonyKey.L8_MALIFIC_DEBILITY: "LC7",
    TestimonyKey.L5_FORTUNATE: "LC8",
    TestimonyKey.L5_MALIFIC_DEBILITY: "LC9",
    TestimonyKey.PERFECTION_DIRECT: "P1",
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: "P2",
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: "P3",
    TestimonyKey.ESSENTIAL_DETRIMENT: "MOD2",
    TestimonyKey.ACCIDENTAL_RETROGRADE: "MOD3",
}

WEIGHT_TABLE: dict[TestimonyKey, float] = {
    token: abs(get_rule_weight(rule_id))
    for token, rule_id in TOKEN_RULE_MAP.items()
}


# ``family``/``kind`` tagging for group-based contribution control
FAMILY_TABLE: dict[TestimonyKey, str] = {
    TestimonyKey.PERFECTION_DIRECT: "perfection",
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: "perfection",
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: "perfection",
    TestimonyKey.L7_FORTUNATE: "l7_condition",
    TestimonyKey.L7_MALIFIC_DEBILITY: "l7_condition",
    TestimonyKey.L2_FORTUNATE: "l2_condition",
    TestimonyKey.L2_MALIFIC_DEBILITY: "l2_condition",
    TestimonyKey.L8_FORTUNATE: "l8_condition",
    TestimonyKey.L8_MALIFIC_DEBILITY: "l8_condition",
    TestimonyKey.L5_FORTUNATE: "l5_condition",
    TestimonyKey.L5_MALIFIC_DEBILITY: "l5_condition",
}

KIND_TABLE: dict[TestimonyKey, str] = {
    TestimonyKey.PERFECTION_DIRECT: "direct",
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: "tol",
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: "col",
    TestimonyKey.L7_FORTUNATE: "l7",
    TestimonyKey.L7_MALIFIC_DEBILITY: "l7",
    TestimonyKey.L2_FORTUNATE: "l2",
    TestimonyKey.L2_MALIFIC_DEBILITY: "l2",
    TestimonyKey.L8_FORTUNATE: "l8",
    TestimonyKey.L8_MALIFIC_DEBILITY: "l8",
    TestimonyKey.L5_FORTUNATE: "l5",
    TestimonyKey.L5_MALIFIC_DEBILITY: "l5",
}

