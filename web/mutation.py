from graphene import ObjectType

from web.mutations.auth import Login, Refresh, Register
from web.mutations.posts import Like, Dislike, Cooked, Uncooked


class Mutation(ObjectType):
    login = Login.Field()
    register = Register.Field()
    refresh = Refresh.Field()
    like = Like.Field()
    dislike = Dislike.Field()
    cooked = Cooked.Field()
    uncooked = Uncooked.Field()
