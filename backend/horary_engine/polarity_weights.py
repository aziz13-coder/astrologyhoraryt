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
    PERFECTION_DIRECT = "perfection_direct"
    PERFECTION_TRANSLATION_OF_LIGHT = "perfection_translation_of_light"
    PERFECTION_COLLECTION_OF_LIGHT = "perfection_collection_of_light"
    ESSENTIAL_DETRIMENT = "essential_detriment"
    ACCIDENTAL_RETROGRADE = "accidental_retrograde"


# Prevent pytest from collecting the enum as a test class
TestimonyKey.__test__ = False


# Mapping of testimony tokens to rule identifiers used for weight lookup
TOKEN_RULE_MAP: dict[TestimonyKey, str] = {
    TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN: "M1",
    TestimonyKey.MOON_APPLYING_SQUARE_EXAMINER_SUN: "M2",
    TestimonyKey.MOON_APPLYING_SEXTILE_EXAMINER_SUN: "M3",
    TestimonyKey.MOON_APPLYING_SEXTILE_L1: "M4",
    TestimonyKey.MOON_APPLYING_SEXTILE_L7: "M5",
    TestimonyKey.MOON_APPLYING_OPPOSITION_EXAMINER_SUN: "M6",
    TestimonyKey.MOON_APPLYING_OPPOSITION_L1: "M7",
    TestimonyKey.MOON_APPLYING_OPPOSITION_L7: "M8",
    TestimonyKey.L10_FORTUNATE: "F1",
    TestimonyKey.PERFECTION_DIRECT: "P1",
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: "P2",
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: "P3",
    TestimonyKey.ESSENTIAL_DETRIMENT: "MOD2",
    TestimonyKey.ACCIDENTAL_RETROGRADE: "MOD3",
}


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
    # Perfection testimonies are positive by default
    TestimonyKey.PERFECTION_DIRECT: Polarity.POSITIVE,
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: Polarity.POSITIVE,
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: Polarity.POSITIVE,
    # Debility indicators
    TestimonyKey.ESSENTIAL_DETRIMENT: Polarity.NEGATIVE,
    TestimonyKey.ACCIDENTAL_RETROGRADE: Polarity.NEGATIVE,
}

WEIGHT_TABLE: dict[TestimonyKey, float] = {
    token: abs(get_rule_weight(rule_id)) for token, rule_id in TOKEN_RULE_MAP.items()
}


# ``family``/``kind`` tagging for group-based contribution control
FAMILY_TABLE: dict[TestimonyKey, str] = {
    TestimonyKey.PERFECTION_DIRECT: "perfection",
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: "perfection",
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: "perfection",
}

KIND_TABLE: dict[TestimonyKey, str] = {
    TestimonyKey.PERFECTION_DIRECT: "direct",
    TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT: "tol",
    TestimonyKey.PERFECTION_COLLECTION_OF_LIGHT: "col",
}

