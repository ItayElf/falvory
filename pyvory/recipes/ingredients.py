from __future__ import annotations

from dataclasses import dataclass, field
from abc import ABC
from typing import Union

from pyvory.recipes import Volume, Weight


@dataclass
class Ingredient(ABC):
    """Base class for all ingredients"""
    name: str
    quantity: float
    units: Union[str, Volume, Weight] = field(init=False)

    @staticmethod
    def from_tup(tup) -> Ingredient:
        name, quantity, units = tup
        if units in [u.name for u in Volume]:
            units = Volume[units]
            return VolumeIngredient(name, quantity, units)
        elif units in [u.name for u in Weight]:
            units = Weight[units]
            return WeightIngredient(name, quantity, units)
        else:
            return AbstractIngredient(name, quantity, units)


@dataclass
class VolumeIngredient(Ingredient):
    """Represents an ingredient that is measured in volume"""
    units: Volume

    def __post_init__(self):
        if not isinstance(self.units, Volume):
            raise ValueError("Non volume units for VolumeIngredient")

    def convert(self, unit: Volume):
        """Converts the ingredient to a new volume unit"""
        if not isinstance(unit, Volume):
            raise ValueError("Non volume units for VolumeIngredient")
        self.quantity *= self.units.value
        self.units = unit
        self.quantity = round(self.quantity / self.units.value, 2)


@dataclass
class WeightIngredient(Ingredient):
    """Represents an ingredient that is measured in volume"""
    units: Weight

    def __post_init__(self):
        if not isinstance(self.units, Weight):
            raise ValueError("Non weight units for WeightIngredient")

    def convert(self, unit: Weight):
        """Converts the ingredient to a new volume unit"""
        if not isinstance(unit, Weight):
            raise ValueError("Non weight units for WeightIngredient")
        self.quantity *= self.units.value
        self.units = unit
        self.quantity = round(self.quantity / self.units.value, 2)


@dataclass
class AbstractIngredient(Ingredient):
    """Represents an ingredient that is measured in a unit that is not convertible such as "a pinch" or "2 carrots" """
    units: str
