from graphene import ObjectType

from web.mutations.auth import Login, Refresh, Register


class Mutation(ObjectType):
    login = Login.Field()
    register = Register.Field()
    refresh = Refresh.Field()
