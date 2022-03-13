from flask_graphql_auth import create_access_token, create_refresh_token
from graphene import Mutation, String

from pyvory.orm.users import login


class Auth(Mutation):
    access_token = String(required=True)
    refresh_token = String(required=True)

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(_, __, email, password):
        if not login(email, password):
            raise Exception("Auth failed: user is not registered.")
        return Auth(access_token=create_access_token(email), refresh_token=create_refresh_token(email))
