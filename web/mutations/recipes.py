import json

from flask_graphql_auth import get_jwt_data
from graphene import Mutation, Field, String, Int

from pyvory.orm.recipes import get_recipe_by_id, update_recipe
from pyvory.recipes.ingredients import Ingredient
from pyvory.recipes.recipe import Recipe
from web.object_types.recipe_object import RecipeObject


class UpdateRecipe(Mutation):
    recipe = Field(RecipeObject, required=True)

    class Arguments:
        token = String(required=True)
        author = String(required=True)
        title = String(required=True)
        description = String(required=True)
        ingredients = String(required=True, description="Ingredient[] as json")
        steps = String(required=True)
        cooking_time = Int()
        servings = String()
        idx = Int(required=True)
        image = String()

    @staticmethod
    def mutate(_, __, token, author, title, description, ingredients, steps, cooking_time, servings, idx, image):
        current_user_email = get_jwt_data(token, "access")["identity"]
        ingredients = [Ingredient.from_tup((i["name"], i["quantity"], i["units"])) for i in json.loads(ingredients)]
        cooking_time = cooking_time if cooking_time else None
        servings = servings if servings else None
        recipe = Recipe(author, title, description, ingredients, json.loads(steps), cooking_time, servings, idx)
        return UpdateRecipe(recipe=update_recipe(current_user_email, recipe, image))
