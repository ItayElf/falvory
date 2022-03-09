import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from pyvory.recipes import Volume, Weight
from pyvory.recipes.ingredients import Ingredient, AbstractIngredient, VolumeIngredient, WeightIngredient


@dataclass
class Recipe:
    """A class that stores a recipe"""
    author: str  # name of the user who posted
    title: str
    description: str
    ingredients: List[Ingredient]
    steps: List[str]
    cooking_time: Optional[int]  # minutes
    servings: Optional[str]
    idx: Optional[int] = field(init=False)

    def scale(self, factor: float):
        """Scales the ingredients and servings by a factor"""
        for i in range(len(self.ingredients)):
            self.ingredients[i].quantity *= factor
        # self.servings *= factor
        nums = {n: int(n) * factor for n in re.findall(r"\d+?", self.servings)}
        keys = sorted(nums.keys(), key=lambda x: int(x), reverse=factor > 1)
        for k in keys:
            self.servings = self.servings.replace(k, str(nums[k]) if nums[k] % 1 else str(int(nums[k])))

    def convert(self, units_map: Dict[str, str], to_celsius: bool):
        """Converts the recipe using a units_map and temperature units. Raises KeyError if invalid unit was used."""
        new_ingredients = []
        for i in self.ingredients:
            if not isinstance(i, AbstractIngredient) and i.units.name in units_map:
                if isinstance(i, VolumeIngredient):
                    i.convert(Volume[units_map[i.units.name]])
                elif isinstance(i, WeightIngredient):
                    i.convert(Weight[units_map[i.units.name]])
            new_ingredients.append(i)
        self.ingredients = new_ingredients
        self.steps = replace_temperature(self.steps, to_celsius)


def replace_temperature(steps: List[str], to_celsius: bool) -> List[str]:
    """Replaces celsius with fahrenheit in a string or vice versa"""
    regex = r"(\d+?)[ ]?{}\b"
    d = {"C": "F", "c": "f", "celsius": "fahrenheit", "Celsius": "Fahrenheit"}
    if to_celsius:
        d = {v: k for k, v in d.items()}
    new_steps = []
    for step in steps:
        for k in d:
            for m in re.finditer(regex.format(k), step, re.MULTILINE):
                val = int(m.groups()[0])
                new = round((val * 9 / 5) + 32 if not to_celsius else ((val - 32) * 5 / 9))
                step = step.replace(m.group(0), m.group(0).replace(k, d[k]).replace(str(val), str(new)))
        new_steps.append(step)
    return new_steps
