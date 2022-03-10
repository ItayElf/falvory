from graphene import ObjectType, Field, Int

from pyvory.orm.recipes import get_recipe_by_id
from web.object_types.recipe_object import RecipeObject


class Query(ObjectType):
    recipe = Field(RecipeObject, idx=Int(required=True))

    @staticmethod
    def resolve_recipe(_, __, idx):
        return get_recipe_by_id(idx)
