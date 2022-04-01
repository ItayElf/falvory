from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from pyvory.recipes import Volume, Weight
from pyvory.recipes.ingredients import Ingredient


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
    idx: Optional[int] = None

    @classmethod
    def from_tup(cls, tup: tuple) -> Recipe:
        idx, author, title, description, steps, cooking_time, servings, name_concat, quantity_concat, units_concat = tup
        steps = json.loads(steps)
        ings = [Ingredient.from_tup((n, float(q), u)) for (n, q, u) in
                zip(name_concat.split("~"), quantity_concat.split("~"), units_concat.split("~"))]
        return cls(author, title, description, ings, steps, cooking_time, servings, idx)


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
