from pyvory.orm import DBConnect
from pyvory.recipes.recipe import Recipe

_get_recipe_base = """
SELECT r.id, r.author, r.title, r.description, r.steps, r.cooking_time, r.servings, GROUP_CONCAT(i.name, '~'), GROUP_CONCAT(i.quantity, '~'), GROUP_CONCAT(i.units, '~')
FROM recipes r 
JOIN ingredients i ON i.recipe_id = r.id
"""


def get_recipe_by_id(idx: int) -> Recipe:
    """Returns a recipe by its id from the db"""
    with DBConnect() as c:
        c.execute(_get_recipe_base + "WHERE r.id=?", (idx,))
        tup = c.fetchone()
    if not tup:
        raise FileNotFoundError(f"No recipe with id {idx}")
    return Recipe.from_tup(tup)
