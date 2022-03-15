from graphene import ObjectType, Int, String, List


class UserObject(ObjectType):
    idx = Int(required=True)
    name = String(required=True)
    bio = String(required=True)
    link = String(required=True)
    followers = List(Int, required=True)
    following = List(Int, required=True)
    posts = List(Int, required=True)
    cookbooks: List(Int, required=True)
