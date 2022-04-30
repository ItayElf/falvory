from graphene import ObjectType
from web.mutations import posts, auth, recipes


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
    update_recipe = recipes.UpdateRecipe.Field()
    make_post = posts.MakePost.Field()
    edit_user = auth.EditUser.Field()
    delete_post = posts.DeletePost.Field()
    delete_comment = posts.DeleteComment.Field()
