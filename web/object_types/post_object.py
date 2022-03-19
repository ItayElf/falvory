from graphene import ObjectType, String, Field, List, Int

from web.object_types.comment_object import CommentObject
from web.object_types.recipe_object import RecipeObject


class PostObject(ObjectType):
    poster = String(required=True)
    recipe = Field(RecipeObject, required=True)
    comments = List(CommentObject, required=True)
    likes = List(String, required=True)
    cooked = List(String, required=True)
    timestamp = Int(required=True)
    idx = Int(required=True)
