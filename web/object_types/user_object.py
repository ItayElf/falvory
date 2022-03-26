from graphene import ObjectType, Int, String, List


class UserObject(ObjectType):
    idx = Int(required=True)
    name = String(required=True)
    bio = String(required=True)
    link = String(required=True)
    followers = List(String, required=True)
    following = List(String, required=True)
    posts = List(Int, required=True)
    cookbooks: List(Int, required=True)
