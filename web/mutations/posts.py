import json

from graphene import Mutation, Boolean, String, Int, Field
from flask_graphql_auth import get_jwt_data

from pyvory.orm.posts import like, dislike, cooked, uncooked, comment as comment_orm, insert_post, delete_post
from pyvory.orm.users import get_user_by_email
from pyvory.recipes.ingredients import Ingredient
from pyvory.recipes.recipe import Recipe
from pyvory.social import Post
from web.object_types.comment_object import CommentObject
from web.object_types.post_object import PostObject


class Like(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        post = Int(required=True)

    @staticmethod
    def mutate(_, __, token, post):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Like(success=like(current_user_email, post))


class Dislike(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        post = Int(required=True)

    @staticmethod
    def mutate(_, __, token, post):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Dislike(success=dislike(current_user_email, post))


class Cooked(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        post = Int(required=True)

    @staticmethod
    def mutate(_, __, token, post):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Cooked(success=cooked(current_user_email, post))


class Uncooked(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        post = Int(required=True)

    @staticmethod
    def mutate(_, __, token, post):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Uncooked(success=uncooked(current_user_email, post))


class Comment(Mutation):
    comment = Field(CommentObject, required=True)

    class Arguments:
        token = String(required=True)
        post = Int(required=True)
        content = String(required=True)

    @staticmethod
    def mutate(_, __, token, post, content):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Comment(comment=comment_orm(current_user_email, post, content))


class MakePost(Mutation):
    post = Field(PostObject, required=True)

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
        image = String(required=False)

    @staticmethod
    def mutate(_, __, token, author, title, description, ingredients, steps, cooking_time, servings, idx, image=""):
        current_user_email = get_jwt_data(token, "access")["identity"]
        ingredients = [Ingredient.from_tup((i["name"], i["quantity"], i["units"])) for i in json.loads(ingredients)]
        cooking_time = cooking_time if cooking_time else None
        servings = servings if servings else None
        recipe = Recipe(author, title, description, ingredients, json.loads(steps), cooking_time, servings, idx)
        poster = get_user_by_email(current_user_email)
        post = Post(poster.name, recipe, [], [], [], 0)
        return MakePost(post=insert_post(current_user_email, post, image))


class DeletePost(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        post = Int(required=True)

    @staticmethod
    def mutate(_, __, token, post):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return DeletePost(success=delete_post(current_user_email, post))
