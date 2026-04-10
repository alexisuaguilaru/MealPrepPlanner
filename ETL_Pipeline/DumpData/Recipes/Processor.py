import pandas as pd
from uuid import uuid4

from .Cleaner import CleanFieldsRecipe
from ...Utils import GatherRecipes

ColumnsRecipe = [
    'Name',
    'TotalTime',
    'Servings',
    'Instructions',
    'Image',
    'Source',
    'Calories',
    'Carbohydrates',
    'Proteins',
    'Fats',
]
NotNullColumns = [
    'Name',
    'TotalTime',
    'Servings',
    'Instructions',
    'Source',
]
def ProcessData(DatasetRecipes):
    RecipesRaw = []
    for recipe in GatherRecipes():
        clean_recipe = CleanFieldsRecipe(recipe)
        RecipesRaw.append(clean_recipe)

    RecipesDataFrame = pd.DataFrame(RecipesRaw,columns=ColumnsRecipe)
    RecipesDataFrame.dropna(subset=NotNullColumns,inplace=True)
    RecipesDataFrame['id'] = RecipesDataFrame['Name'].apply(lambda value: uuid4())
    RecipesDataFrame.dropna(subset=NotNullColumns,inplace=True)

    RecipesDataFrame.to_csv(DatasetRecipes,index=False)
    return RecipesDataFrame