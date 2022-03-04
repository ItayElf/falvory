from enum import Enum


class Volume(Enum):
    """Stores volume units"""
    milliliter = 1
    liter = 1000
    tbsp = 14.7868
    tsp = 4.92892
    cup = 240
    pint = 473.176
    floz = 29.5735


class Weight(Enum):
    """Stores weight units"""
    gram = 1
    kg = 1000
    lb = 453.592
    oz = 28.3495
