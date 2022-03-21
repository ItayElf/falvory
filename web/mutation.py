from graphene import ObjectType
from web.mutations import posts, auth


class Mutation(ObjectType):
    login = auth.Login.Field()
    register = auth.Register.Field()
    refresh = auth.Refresh.Field()
    like = posts.Like.Field()
    dislike = posts.Dislike.Field()
    cooked = posts.Cooked.Field()
    uncooked = posts.Uncooked.Field()
    comment = posts.Comment.Field()
    follow = auth.Follow.Field()
    unfollow = auth.Unfollow.Field()
