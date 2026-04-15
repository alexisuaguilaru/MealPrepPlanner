import re
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
import pandas as pd
from sqlalchemy.exc import IntegrityError

from ..Utils import DumpDataFrameToSQL
from ...Database import CreateConnectionToAPI
from ...Database.Connector import SCHEMA_DB

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

def ProcessRelations_RecipesNutrients():
    ConnectionAPI = CreateConnectionToAPI('reader_data')

    SelectQuery = (
        'id, '
        'Servings, '
        'RECIPES_INGREDIENTS(UnitMeasurement,NumericAmount,INGREDIENTS(Calories,Carbohydrates,Proteins,Fats,INGREDIENTS_NUTRIENTS(Amount,nutrient_id)))'
    )
    RecipesNutrients = ConnectionAPI.from_('RECIPES').select(SelectQuery).execute().data

    return map(_ProcessRecipeNutrients,RecipesNutrients)

def ProcessMissingRecipes_Macronutrients():
    DatasetRecipes_Macronutrients = Path('./Datasets/SQL/Recipes_Macronutrients.csv')
    UpdateDataFrameRecipesMacronutrients = pd.read_csv(DatasetRecipes_Macronutrients,index_col='id')

    ConnectionAPI = CreateConnectionToAPI('reader_data')
    SelectQuery = (
        'id, '
        'Calories, '
        'Carbohydrates, '
        'Proteins, '
        'Fats'
    )
    ResponseRecipesMacronutrients = ConnectionAPI.from_('RECIPES').select(SelectQuery).execute().data
    CurrentDataFrameRecipesMacronutrients = pd.DataFrame(ResponseRecipesMacronutrients)

    for recipe in CurrentDataFrameRecipesMacronutrients.iloc:
        missing_values = (recipe != recipe)
        missing_fields = recipe[missing_values].index
        if 0 < len(missing_fields):
            recipe_id = recipe['id']
            tuple_update_values = UpdateDataFrameRecipesMacronutrients.loc[recipe_id,missing_fields].items()
            statement_format = map(lambda tuple_values: '"{}"={}'.format(*tuple_values),tuple_update_values)
            set_statement = ', '.join(statement_format)
            query_statement = f"""UPDATE "{SCHEMA_DB}"."RECIPES" SET {set_statement} WHERE id='{recipe_id}';"""
            yield recipe_id , query_statement          

    
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

def _ProcessRecipeNutrients(Recipe):
    ServingSizeProportion = 100
    RecipeMacronutrientsList = []
    RecipeMicronutrientsList = []

    for recipe_ingredients in Recipe['RECIPES_INGREDIENTS']:
        ingredient = recipe_ingredients['INGREDIENTS']

        ingredient_nutrients = ingredient['INGREDIENTS_NUTRIENTS']
        ingredient_micronutrients = pd.DataFrame(ingredient_nutrients)
        ingredient_micronutrients['recipe_id'] = Recipe['id']

        macronutrients = {
            'Calories': ingredient['Calories'],
            'Carbohydrates': ingredient['Carbohydrates'],
            'Proteins': ingredient['Proteins'],
            'Fats': ingredient['Fats'],
        }
        ingredient_macronutrients = pd.DataFrame(macronutrients,index=[0])

        unit_recipe , adj_multi = _GetUnitLemmaMultiplier(recipe_ingredients['UnitMeasurement'])
        adj_conversion_factor = adj_multi*_GetConversionFactor(unit_recipe,'gr')/ServingSizeProportion/Recipe['Servings']

        ingredient_macronutrients *= adj_conversion_factor
        ingredient_macronutrients['id'] = Recipe['id']
        RecipeMacronutrientsList.append(ingredient_macronutrients.set_index('id'))

        ingredient_micronutrients['Amount'] *= adj_conversion_factor
        RecipeMicronutrientsList.append(ingredient_micronutrients.set_index(['recipe_id','nutrient_id']))

    RecipesMacronutrients = sum(RecipeMacronutrientsList)
    RecipeMicronutrients = sum(RecipeMicronutrientsList)
    return RecipesMacronutrients.reset_index() , RecipeMicronutrients.reset_index()