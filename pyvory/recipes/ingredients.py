from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Ingredient:
    """Base class for all ingredients"""
    name: str
    quantity: float
    units: str

    @staticmethod
    def from_tup(tup) -> Ingredient:
        return Ingredient(*tup)
