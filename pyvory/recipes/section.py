from dataclasses import dataclass
from typing import List

from pyvory.recipes.recipe import Recipe


@dataclass
class Section:
    """Represent a section of a cookbook"""
    title: str
    recipes: List[Recipe]
    color: str  # hex rgb color with '#'
