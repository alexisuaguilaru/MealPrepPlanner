import re
from collections import defaultdict
from fractions import Fraction
import pandas as pd

from ...Database import CreateConnectionToAPI

def ProcessRelations_RecipesPrices():
    ConnectionAPI = CreateConnectionToAPI('reader_data')
    
    SelectQuery = (
        'id, '
        'Servings, '
        'RECIPES_INGREDIENTS(UnitMeasurement,NumericAmount,INGREDIENTS(INGREDIENTS_PRICES(Price,Unit)))'
    )
    RecipesIngredientsPrices = ConnectionAPI.from_('RECIPES').select(SelectQuery).execute().data

    DatasetRecipesPrices = list(map(_ProcessRecipePrice,RecipesIngredientsPrices))
    DataFrameRecipesPrices = pd.DataFrame(
        DatasetRecipesPrices,
        columns = ['id','PricePerServing'],
    )

    return DataFrameRecipesPrices
    
def _ProcessRecipePrice(Recipe):
    RecipePrice = 0
    for ingredient in Recipe['RECIPES_INGREDIENTS']:
        unit_recipe , adj_multi = _GetUnitLemmaMultiplier(ingredient['UnitMeasurement'])
        ingredient_data = ingredient['INGREDIENTS']['INGREDIENTS_PRICES']
        unit_ingredient = ingredient_data['Unit']

        adj_conversion_factor = adj_multi*_GetConversionFactor(unit_recipe,unit_ingredient)
        total_ingredient_price = ingredient_data['Price']*adj_conversion_factor*ingredient['NumericAmount']
        RecipePrice += total_ingredient_price
    return Recipe['id'] , RecipePrice/Recipe['Servings']

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

Pattern_MultUnit = r"(?P<mult>[\d\.\/]+).*?(?P<unit>ounce|pound|pinch|inch|cup|bag|can|packet|tablespoon|teaspoon|slice|whole|box|cucharada|cucharadita|taza|kilogramo|gramo|gr|kilo|kg|caja|lt|ml|mm|pieza|caja)"
Pattern_Unit = r".*?(?P<unit>ounce|pound|pinch|inch|cup|bag|can|packet|tablespoon|teaspoon|slice|whole|box|cucharada|cucharadita|taza|kilogramo|gramo|gr|kilo|kg|caja|lt|ml|mm|pieza|caja)"
def _GetUnitLemmaMultiplier(Unit):
    BaseUnit = 'piece'
    Multiplier = 1

    if not Unit:
        BaseUnit = 'piece'
        Multiplier = 1
    elif (Match_MultUnit:=re.search(Pattern_MultUnit,Unit)):
        BaseUnit = Match_MultUnit.group('unit')
        Multiplier = Match_MultUnit.group('mult')
    elif (Match_Uni:=re.search(Pattern_Unit,Unit)):
        BaseUnit = Match_Uni.group('unit')

    return BaseUnit , float(Fraction(Multiplier))

def _GetConversionFactor(FromUnit,ToUnit):
    return ConversionUnits[FromUnit]/ConversionUnits[ToUnit]