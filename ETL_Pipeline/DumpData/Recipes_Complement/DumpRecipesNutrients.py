from pathlib import Path
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessRelations_RecipesNutrients , ProcessMissingRecipes_Macronutrients
from ..Utils import DumpDataFrameToSQL
from ...Database import CreateConnectionToSQL , CreateConnectionToAPI
from ...Database.Connector import SCHEMA_DB

def MainDumpRecipesNutrients(MainLogger):
    DatasetRecipesNutrients = Path('./Datasets/SQL/RecipesNutrients.csv')
    DatasetRecipes_Macronutrients = Path('./Datasets/SQL/Recipes_Macronutrients.csv')

    if not DatasetRecipesNutrients.exists():
        DataFrameRecipesIngredients_List = []
        DataFrameRecipes_Macronutrients_List = []
        for index , (recipe_macronutrients,recipe_micronutrients) in enumerate(ProcessRelations_RecipesNutrients()):
            DataFrameRecipesIngredients_List.append(recipe_micronutrients)
            DataFrameRecipes_Macronutrients_List.append(recipe_macronutrients)
            try:
                DumpDataFrameToSQL(recipe_micronutrients,'RECIPES_NUTRIENTS')
            except IntegrityError:
                MainLogger.info(f'Recipes_Nutrients Relations {index} Data Preloaded')

        DataFrameRecipesNutrients = pd.concat(DataFrameRecipesIngredients_List)
        DataFrameRecipesNutrients.to_csv(DatasetRecipesNutrients,index=False)

        DataFrameRecipes_Macronutrients = pd.concat(DataFrameRecipes_Macronutrients_List)
        DataFrameRecipes_Macronutrients.to_csv(DatasetRecipes_Macronutrients,index=False)

    else:
        DataFrameRecipesNutrients = pd.read_csv(DatasetRecipesNutrients)
        try:
            DumpDataFrameToSQL(DataFrameRecipesNutrients,'RECIPES_NUTRIENTS')
        except IntegrityError:
            MainLogger.info(f'Recipes_Nutrients Relations Data Preloaded')

    with CreateConnectionToSQL().begin() as ConnectionToSQL:
        for recipe_id , set_sql_statement in ProcessMissingRecipes_Macronutrients():
            try:
                set_sql = text(set_sql_statement)
                ConnectionToSQL.execute(set_sql)
            except IntegrityError:
                MainLogger.info(f'Recipe {recipe_id} Macronutrients Preloaded')