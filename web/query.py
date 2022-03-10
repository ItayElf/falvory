from graphene import ObjectType, String


class Query(ObjectType):
    hello = String(name=String(required=True), required=True)

    @staticmethod
    def resolve_hello(root, info, name):
        return f"Hello {name}!"
