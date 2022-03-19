from typing import Tuple

from graphene import ObjectType, String


class SuggestionObject(ObjectType):
    followed_by = String(required=True)
    suggested = String(required=True)

    @staticmethod
    def resolve_followed_by(parent: Tuple[str, str], _):
        return parent[0]

    @staticmethod
    def resolve_suggested(parent: Tuple[str, str], _):
        return parent[1]
