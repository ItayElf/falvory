from flask_graphql_auth import get_jwt_data
from graphene import ObjectType, Field, Int, String, List

from pyvory.orm.posts import get_feed, get_post, get_posts_of, get_cooked_by, search_posts, explore_posts
from pyvory.orm.recipes import get_recipe_by_id
from pyvory.orm.users import get_user_by_email, get_suggestions, get_user_by_name, search_users
from web.object_types.post_object import PostObject
from web.object_types.recipe_object import RecipeObject
from web.object_types.search_object import SearchObject
from web.object_types.suggestion_object import SuggestionObject
from web.object_types.user_object import UserObject


class Query(ObjectType):
    recipe = Field(RecipeObject, idx=Int(required=True), required=True)
    current_user = Field(UserObject, token=String(required=True))
    feed = List(PostObject, token=String(required=True), items=Int(required=True), offset=Int(required=True))
    suggestions = List(SuggestionObject, token=String(required=True), required=True)
    post = Field(PostObject, required=True, idx=Int(required=True))
    user = Field(UserObject, required=True, name=String(required=True))
    posts_of = List(PostObject, name=String(required=True))
    cooked_by = List(PostObject, name=String(required=True))
    search = Field(SearchObject, query=String(required=True))
    explore = List(PostObject, seed=Int(required=True), items=Int(required=True), offset=Int(required=True))

    @staticmethod
    def resolve_recipe(_, __, idx):
        return get_recipe_by_id(idx)

    @staticmethod
    def resolve_current_user(_, __, token):
        current_user_email = get_jwt_data(token, "access")["identity"]
        try:
            return get_user_by_email(current_user_email)
        except FileNotFoundError:
            raise Exception("No logged user")

    @staticmethod
    def resolve_feed(_, __, token, items, offset):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return get_feed(current_user_email, items, offset)

    @staticmethod
    def resolve_suggestions(_, __, token):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return get_suggestions(current_user_email)

    @staticmethod
    def resolve_post(_, __, idx):
        return get_post(idx)

    @staticmethod
    def resolve_user(_, __, name):
        return get_user_by_name(name)

    @staticmethod
    def resolve_posts_of(_, __, name):
        return get_posts_of(name)

    @staticmethod
    def resolve_cooked_by(_, __, name):
        return get_cooked_by(name)

    @staticmethod
    def resolve_search(_, __, query):
        return search_posts(query), search_users(query)

    @staticmethod
    def resolve_explore(_, __, seed, items, offset):
        return explore_posts(seed, items, offset)
