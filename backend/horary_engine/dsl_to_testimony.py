"""Dispatch DSL primitives to testimony tokens with metadata."""
from __future__ import annotations

from typing import Any, Dict, List

from .dsl import (
    Aspect,
    Translation,
    Reception,
    EssentialDignity,
    Role,
    Moon,
    L10,
)
try:  # pragma: no cover - allow running as script
    from ..models import Planet, Aspect as AspectType
except ImportError:  # pragma: no cover
    from models import Planet, Aspect as AspectType

from .polarity_weights import TestimonyKey

Dispatch = Dict[str, Any]


def _collect_roles(obj: Any) -> List[str]:
    roles: List[str] = []
    for attr in ("actor", "receiver", "received", "translator", "from_actor", "to_actor", "actor1", "actor2"):
        value = getattr(obj, attr, None)
        if isinstance(value, Role):
            roles.append(value.name.lower())
    return roles


def _dispatch_aspect(asp: Aspect) -> List[Dispatch]:
    results: List[Dispatch] = []
    if (
        asp.actor1 == Moon
        and asp.actor2 == Planet.SUN
        and asp.aspect == AspectType.TRINE
        and asp.applying
    ):
        results.append(
            {
                "key": TestimonyKey.MOON_APPLYING_TRINE_EXAMINER_SUN,
                "house": None,
                "factor": 1.0,
                "roles": _collect_roles(asp),
            }
        )
    return results


def dispatch(obj: Any) -> List[Dispatch]:
    """Return testimony mappings for a DSL primitive.

    Unrecognized objects return an empty list allowing callers to pass through
    non-DSL values unchanged.
    """
    if isinstance(obj, Aspect):
        return _dispatch_aspect(obj)
    if isinstance(obj, Translation):
        return [
            {
                "key": TestimonyKey.PERFECTION_TRANSLATION_OF_LIGHT,
                "house": None,
                "factor": 1.0,
                "roles": _collect_roles(obj),
            }
        ]
    if isinstance(obj, Reception):
        if obj.receiver == L10:
            return [
                {
                    "key": TestimonyKey.L10_FORTUNATE,
                    "house": 10,
                    "factor": 1.0,
                    "roles": _collect_roles(obj),
                }
            ]
    if isinstance(obj, EssentialDignity):
        if isinstance(obj.score, str) and obj.score.lower() == "detriment":
            return [
                {
                    "key": TestimonyKey.ESSENTIAL_DETRIMENT,
                    "house": None,
                    "factor": 1.0,
                    "roles": _collect_roles(obj),
                }
            ]
    return []


__all__ = ["dispatch"]
