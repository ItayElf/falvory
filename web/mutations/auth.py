import sqlite3

from flask_graphql_auth import create_access_token, create_refresh_token, get_jwt_identity, \
    mutation_jwt_refresh_token_required, get_jwt_data
from graphene import Mutation, String, Boolean, Int

from pyvory.orm.users import login, register, follow, unfollow, update_user


class Login(Mutation):
    access_token = String(required=True)
    refresh_token = String(required=True)

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(_, __, email, password):
        if not login(email, password):
            raise Exception("Auth failed: user is not registered.")
        return Login(access_token=create_access_token(email), refresh_token=create_refresh_token(email))


class Register(Mutation):
    access_token = String(required=True)
    refresh_token = String(required=True)

    class Arguments:
        email = String(required=True)
        password = String(required=True)
        name = String(required=True)

    @staticmethod
    def mutate(_, __, email, password, name):
        register(email, password, name)
        return Register(access_token=create_access_token(email), refresh_token=create_refresh_token(email))


class Refresh(Mutation):
    class Arguments:
        refresh_token = String()

    new_token = String()

    @mutation_jwt_refresh_token_required
    def mutate(self):
        current_user = get_jwt_identity()
        return Refresh(new_token=create_access_token(identity=current_user))


class Follow(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        name = String(required=True)

    @staticmethod
    def mutate(_, __, token, name):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Follow(success=follow(current_user_email, name))


class Unfollow(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        name = String(required=True)

    @staticmethod
    def mutate(_, __, token, name):
        current_user_email = get_jwt_data(token, "access")["identity"]
        return Unfollow(success=unfollow(current_user_email, name))


class EditUser(Mutation):
    success = Boolean(required=True)

    class Arguments:
        token = String(required=True)
        name = String(required=True)
        bio = String(required=True)
        link = String(required=True)
        image = String()

    @staticmethod
    def mutate(_, __, token, name, bio, link, image=None):
        current_user_email = get_jwt_data(token, "access")["identity"]
        try:
            update_user(current_user_email, name, bio, link, image)
            return EditUser(success=True)
        except sqlite3.IntegrityError:
            return EditUser(success=False)
