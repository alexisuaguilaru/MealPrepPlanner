from pathlib import Path
import pandas as pd
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessTabularData , ProcessEmbeddingsData , ProcessPricesData
from ..Utils import DumpDataFrameToSQL , InitSemanticModel
from ...Database import CreateConnectionToAPI

IngredientsTableColumns = [
    'id',
    'Name',
    'Calories',
    'Carbohydrates',
    'Proteins',
    'Fats',
    'Embedding',
    'id_price',
]
NutrientsTableColumns = [
    'Fiber',
    'Calcium',
    'Iron',
    'Zinc',
    'VitaminC',
    'VitaminB1',
    'VitaminB2',
    'VitaminB3',
    'VitaminB6',
    'VitaminB9',
    'VitaminB12',
    'VitaminA',
    'VitaminE',
    'VitaminD',
    'VitaminK',
    'SaturatedFat',
    'MonounsaturatedFat',
    'PolyunsaturatedFat',
    'Cholesterol',
]
def MainDumpIngredients(MainLogger):
    DatasetIngredients_Aux = Path('./Datasets/SQL/Ingredients_Aux.csv')
    DatasetIngredients = Path('./Datasets/SQL/Ingredients.csv')

    if not DatasetIngredients_Aux.exists():
        ProcessTabularData(DatasetIngredients_Aux)

    if not DatasetIngredients.exists():
        DataFrameIngredients_List = []
        SemanticModel = InitSemanticModel()
        ConnectionToAPI = CreateConnectionToAPI('loader_data')

        for index , batch_ingredients in enumerate(ProcessEmbeddingsData(DatasetIngredients_Aux)):
            ProcessPricesData(batch_ingredients,SemanticModel,ConnectionToAPI)
            try:
                DumpDataFrameToSQL(batch_ingredients[IngredientsTableColumns],'INGREDIENTS')
            except IntegrityError:
                MainLogger.info(f'Ingredients {index} Data Preloaded')
            DataFrameIngredients_List.append(batch_ingredients)
        
        DataFrameIngredients = pd.concat(DataFrameIngredients_List,ignore_index=True)
        DataFrameIngredients.to_csv(DatasetIngredients,index=False)
    
    else:
        BatchIngredientsDataFrame = pd.read_csv(DatasetIngredients,chunksize=250)
        for index , batch_data in enumerate(BatchIngredientsDataFrame):
            try:
                DumpDataFrameToSQL(batch_data[IngredientsTableColumns],'INGREDIENTS')
            except IntegrityError:
                MainLogger.info(f'Ingredients Embeddings {index} Data Preloaded')

def MainDumpIngredients_Nutrients(MainLogger):
    DatasetIngredients = Path('./Datasets/SQL/Ingredients.csv')
    DatasetNutrients = Path('./Datasets/SQL/Nutrients.csv')
    DatasetIngredientsNutrients = Path('./Datasets/SQL/Ingredients_Nutrients.csv')

    DataFrameIngredientsNutrients = pd.read_csv(DatasetIngredients)
    DataFrameNutrients = pd.read_csv(DatasetNutrients).set_index('Name')

    if not DatasetIngredientsNutrients.exists():
        DataFrameIngredientsNutrients_List = []
        for nutrient in DataFrameNutrients.index:
            dataframe_ingredients_nutrients = pd.DataFrame()
            dataframe_ingredients_nutrients['ingredient_id'] = DataFrameIngredientsNutrients['id']
            dataframe_ingredients_nutrients['nutrient_id'] = DataFrameNutrients.loc[nutrient,'id']
            dataframe_ingredients_nutrients['Amount'] = DataFrameIngredientsNutrients[nutrient]

            try:
                DumpDataFrameToSQL(dataframe_ingredients_nutrients,'INGREDIENTS_NUTRIENTS')
            except IntegrityError:
                MainLogger.info(f'Ingredients_Nutrients Relations {index} Data Preloaded')

            DataFrameIngredientsNutrients_List.append(dataframe_ingredients_nutrients)
        
        DataFrameIngredientsNutrients = pd.concat(DataFrameIngredientsNutrients_List,ignore_index=True)
        DataFrameIngredientsNutrients.to_csv(DatasetIngredientsNutrients,index=False)

    else:
        DataFrameIngredientsNutrients = pd.read_csv(DatasetIngredientsNutrients)
        try:
            DumpDataFrameToSQL(DataFrameIngredientsNutrients,'INGREDIENTS_NUTRIENTS')
        except IntegrityError:
            MainLogger.info('Ingredients_Nutrients Relations Data Preloaded')