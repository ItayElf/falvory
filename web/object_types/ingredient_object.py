from graphene import ObjectType, String, Float

from pyvory.recipes.ingredients import Ingredient


class IngredientObject(ObjectType):
    name = String(required=True)
    quantity = Float(required=True)
    units = String(required=True)

    # @staticmethod
    # def resolve_name(parent: Ingredient, _):
    #     return parent.name
    #
    # @staticmethod
    # def resolve_quantity(parent: Ingredient, _):
    #     return parent.quantity

    @staticmethod
    def resolve_units(parent: Ingredient, _):
        if type(parent.units) is str:
            return parent.units
        else:
            return parent.units.name
