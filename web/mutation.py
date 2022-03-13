from graphene import ObjectType

from web.mutations.auth import Auth


class Mutation(ObjectType):
    auth = Auth.Field()
