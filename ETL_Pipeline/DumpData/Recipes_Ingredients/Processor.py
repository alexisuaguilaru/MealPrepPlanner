from functools import partial
import pandas as pd
from uuid import uuid4

from .Cleaner import CleanFieldIngredients
from ..Utils import InitSemanticModel
from ...Utils import GatherRecipes
from ...Database import CreateConnectionToAPI

ColumnsRecipeIngredients = [
    'RecipeName',
    'NumericAmount',
    'StringAmount',
    'UnitMeasurement',
    'IngredientName',
]
def ProcessTabularData(DatasetRecipes_Ingredients_Aux):
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

    RecipesIngredientsDataFrame.to_csv(DatasetRecipes_Ingredients_Aux,index=False)
    return RecipesIngredientsDataFrame

ColumnsRecipeIngredientsIDs = [
    'NumericAmount',
    'StringAmount',
    'UnitMeasurement',
    'recipe_id',
]
def ProcessEmbeddingData(DatasetRecipesIngredients):
    SemanticModel = InitSemanticModel()
    ConnectionToAPI = CreateConnectionToAPI('loader_data')

    BatchRecipesIngredientsDataFrame = pd.read_csv(
        DatasetRecipesIngredients,
        chunksize = 250,
    )

    SearchIngredientID = partial(_InitSearchIngredientID,Model=SemanticModel,ConnectionAPI=ConnectionToAPI)
    for batch_data in BatchRecipesIngredientsDataFrame:
        ingredients_recipes = batch_data[ColumnsRecipeIngredientsIDs].copy()
        ingredients_recipes['ingredient_id'] = SearchIngredientID(batch_data['IngredientName'])
        ingredients_recipes['IngredientName'] = batch_data['IngredientName']
        ingredients_recipes['id'] = ingredients_recipes['IngredientName'].apply(lambda value: uuid4())
        yield ingredients_recipes

def _InitSearchIngredientID(IngredientsNames,Model,ConnectionAPI):
    QueryVectors = Model.encode(IngredientsNames.to_list()).tolist()

    IngredientIDs = []
    for query_vector in QueryVectors:
        response = ConnectionAPI.rpc('search_ingredients',{
            'query_vec': query_vector,
            'limit_results': 1,
            'threshold': 0.25,
        }).execute()

        ingredient_id = response.data[0]['id']
        IngredientIDs.append(ingredient_id)
    
    return IngredientIDs