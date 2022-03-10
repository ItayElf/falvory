from graphene import Int, String, List, ObjectType

from .ingredient_object import IngredientObject


class RecipeObject(ObjectType):
    idx = Int(required=True)
    author = String(required=True)
    title = String(required=True)
    description = String(required=True)
    steps = List(String, required=True)
    cooking_time = Int()
    servings = String()
    ingredients = List(IngredientObject, required=True)

    # @staticmethod
    # def resolve_idx(parent: Recipe, _):
    #     return parent.idx
    #
    # @staticmethod
    # def resolve_author(parent: Recipe, _):
    #     return parent.author
    #
    # @staticmethod
    # def resolve_title(parent: Recipe, _):
    #     return parent.title
    #
    # @staticmethod
    # def resolve_description(parent: Recipe, _):
    #     return parent.description
    #
    # @staticmethod
    # def resolve_steps(parent: Recipe, _):
    #     return parent.steps
    #
    # @staticmethod
    # def resolve_cooking_time(parent: Recipe, _):
    #     return parent.cooking_time
    #
    # @staticmethod
    # def resolve_servings(parent: Recipe, _):
    #     return parent.servings
    #
    # @staticmethod
    # def resolve_ingredients(parent: Recipe, _):
    #     return parent.ingredients
