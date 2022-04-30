from graphene import ObjectType, String, Int


class CommentObject(ObjectType):
    commenter = String(required=True)
    content = String(required=True)
    timestamp = Int(required=True)
    idx = Int(required=True)
