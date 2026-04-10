import pandas as pd

from .Cleaner import CleanFieldIngredients
from ...Utils import GatherRecipes

ColumnsRecipeIngredients = [
    'RecipeName',
    'NumericAmount',
    'StringAmount',
    'UnitMeasurement',
    'IngredientName',
]
def ProcessTabularData():
    RecipesIngredientsRaw = []
    for recipe in GatherRecipes():
        clean_recipe_ingredients = CleanFieldIngredients(recipe)
        RecipesIngredientsRaw.extend(clean_recipe_ingredients)

    RecipesIngredientsDataFrame = pd.DataFrame(
        RecipesIngredientsRaw,
        columns = ColumnsRecipeIngredients,
    )

    RecipesDataFrame = pd.read_csv('./Datasets/SQL/Recipes.csv',usecols=['Name','id'])
    RecipesIngredientsDataFrame = RecipesIngredientsDataFrame.merge(
        RecipesDataFrame,
        how = 'inner',
        left_on = 'RecipeName',
        right_on = 'Name',
    )
    RecipesIngredientsDataFrame.drop(columns=['RecipeName','Name'],inplace=True)
    RecipesIngredientsDataFrame.rename(columns={'id':'recipe_id'},inplace=True)

    return RecipesIngredientsDataFrame