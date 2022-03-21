from graphene import Mutation, Boolean, String, Int, Field
from flask_graphql_auth import get_jwt_data

from pyvory.orm.posts import like, dislike, cooked, uncooked, comment as comment_orm
from web.object_types.comment_object import CommentObject


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
