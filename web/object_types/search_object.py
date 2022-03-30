from graphene import ObjectType, List

from web.object_types.post_object import PostObject
from web.object_types.user_object import UserObject


class SearchObject(ObjectType):
    posts = List(PostObject, required=True)
    users = List(UserObject, required=True)

    @staticmethod
    def resolve_posts(parent, _):
        return parent[0]

    @staticmethod
    def resolve_users(parent, _):
        return parent[1]
