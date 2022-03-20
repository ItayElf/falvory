from graphene import Mutation, Boolean, String, Int
from flask_graphql_auth import get_jwt_data

from pyvory.orm.posts import like, dislike


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
        return Like(success=dislike(current_user_email, post))
