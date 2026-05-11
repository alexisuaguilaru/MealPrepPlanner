from collections import defaultdict
from uuid import UUID
import pandas as pd

from .Connection import ConnectionToAPI

ColumnsRecipesIngredients = ['ingredient_id','NumericAmount','IngredientName','UnitMeasurement']
def GetIngredientsInformation(
        PrevRecipesID: list[UUID]
    ):

    IngredientesPricesInformation = (
    ConnectionToAPI
        .from_('RECIPES_INGREDIENTS')
        .select(
            *ColumnsRecipesIngredients,
            'INGREDIENTS(Name,INGREDIENTS_PRICES(Price,Unit))',
            'RECIPES(Servings)'
        )
        .in_('recipe_id',PrevRecipesID)
        .execute()
    ).data

    return pd.DataFrame(map(_CleanIngredientInformation,IngredientesPricesInformation))

def _CleanIngredientInformation(
        Ingredient: dict,
    ):

    Amount = Ingredient['NumericAmount']
    IngredientUnit = Ingredient['UnitMeasurement']
    PriceInformation = Ingredient['INGREDIENTS']['INGREDIENTS_PRICES']
    PriceUnit = PriceInformation['Unit']
    Price = PriceInformation['Price']
    TotalPrice = Amount*_GetConversionFactor(IngredientUnit,PriceUnit)*Price
    return {
        'ingredient_id': Ingredient['ingredient_id'],
        'Name': Ingredient['INGREDIENTS']['Name'],
        'Amount': Amount,
        'UnitMeasurement': IngredientUnit,
        'TotalPrice': TotalPrice,
        'Servings': Ingredient['RECIPES']['Servings'],
    }

BaseUnits = {
    'ounce': 28.35,
    'pound': 453.59,
    'cucharada': 15.0,
    'cucharadita': 5.0,
    'cup': 236.59,
    'gramo': 1.0,
    'kilo': 1000.0,
    'pinch': 0.35,
    'tablespoon': 15.0,
    'taza': 250.0,
    'teaspoon': 5.0,
    'gr': 1.0,
    'kg': 1000.0,
    'lt': 1000.0,
    'ml': 1.0,
}
ConversionUnits = defaultdict(lambda: 100,BaseUnits)
def _GetConversionFactor(FromUnit,ToUnit):
    return ConversionUnits[FromUnit]/ConversionUnits[ToUnit]