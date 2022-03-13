from graphene import ObjectType

from web.mutations.auth import Auth, Refresh


class Mutation(ObjectType):
    auth = Auth.Field()
    refresh = Refresh.Field()
