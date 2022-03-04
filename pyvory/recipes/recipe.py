import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from pyvory.recipes import Volume, Weight
from pyvory.recipes.ingredients import Ingredient, AbstractIngredient, VolumeIngredient, WeightIngredient


@dataclass
class Recipe:
    """A class that stores a recipe"""
    title: str
    description: str
    ingredients: List[Ingredient]
    steps: List[str]
    cooking_time: Optional[int]  # minutes
    servings: Optional[int]
    idx: Optional[int] = field(init=False)

    def scale(self, factor: float):
        """Scales the ingredients by a factor"""
        for i in range(len(self.ingredients)):
            self.ingredients[i].quantity *= factor

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


if __name__ == '__main__':
    ings = [
        WeightIngredient("Butter", 300, Weight.gram),
        VolumeIngredient("Sugar", 2, Volume.cup),
        VolumeIngredient("Molasses", 1, Volume.tbsp),
        AbstractIngredient("Eggs", 2, "")
    ]
    steps = [
        'Melt the butter completely before mixing in the sugar, molasses, eggs, and vanilla until smooth. Mix in the baking soda and two cups of the flour. Add more flour until dough appears wet but is not terribly sticky. Refrigerate dough for at least 30 min.',
        'Pre-heat oven to 375 Fahrenheit.',
        'Form the chilled dough into balls the size of golf balls. Smash them into the shapes of hockey pucks and place them on parchment-lined baking sheets. This should yield about 18 big cookies, spread across three pans.',
        'Turn on the broiler and broil the tops of the cookies, one pan at a time on a high rack, until golden. Return the oven to 375 f on its baking mode, allow the broiler to cool for a moment, then bake the cookies for 10-12 minutes.'
    ]
    r = Recipe("Broiled Chocolate Chip Cookies", "", ings, steps, None, None)
    r.convert({"gram": "oz", "cup": "pint"}, True)
    print(r.ingredients)
    print(r.steps)
