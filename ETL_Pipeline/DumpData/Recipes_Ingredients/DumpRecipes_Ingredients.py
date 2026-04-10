from pathlib import Path
import pandas as pd 
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessTabularData , ProcessEmbeddingData
from ..Utils import DumpDataFrameToSQL

def MainDumpRecipes_Ingredients(MainLogger):
    DatasetRecipesIngredients_Aux = Path('./Datasets/SQL/RecipesIngredients_Aux.csv')
    DatasetRecipesIngredients = Path('./Datasets/SQL/RecipesIngredients.csv')
    
    if not DatasetRecipesIngredients_Aux.exists():
        ProcessTabularData(DatasetRecipesIngredients_Aux)

    if not DatasetRecipesIngredients.exists():
        RecipesIngredientsDataFrame_List = []
        for index , batch_ingredients_recipes in enumerate(ProcessEmbeddingData(DatasetRecipesIngredients_Aux)):
            try: 
                DumpDataFrameToSQL(batch_ingredients_recipes,'RECIPES_INGREDIENTS')
            except IntegrityError:
                MainLogger.info(f'Recipes_Ingredients Relations {index} Data Preloaded')
            RecipesIngredientsDataFrame_List.append(batch_ingredients_recipes)
        
        RecipesIngredientsDataFrame = pd.concat(RecipesIngredientsDataFrame_List,ignore_index=True)
        RecipesIngredientsDataFrame.to_csv(DatasetRecipesIngredients,index=False)
    else:
        BatchRecipesIngredientsDataFrame = pd.read_csv(DatasetRecipesIngredients,chunksize=250)
        for index , batch_ingredients_recipes in enumerate(BatchRecipesIngredientsDataFrame):
            DumpDataFrameToSQL(batch_ingredients_recipes,'RECIPES_INGREDIENTS')
            try:
                DumpDataFrameToSQL(batch_ingredients_recipes,'RECIPES_INGREDIENTS')
            except IntegrityError:
                MainLogger.info(f'Recipes_Ingredients Relations {index} Data Preloaded')