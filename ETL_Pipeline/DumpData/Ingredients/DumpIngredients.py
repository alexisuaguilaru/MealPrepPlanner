from pathlib import Path
import pandas as pd
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessTabularData , ProcessEmbeddingsData
from ..Utils import DumpDataFrameToSQL

def MainDumpIngredients(MainLogger):
    DatasetIngredients_Aux = Path('./Datasets/SQL/Ingredients_Aux.csv')
    DatasetIngredients = Path('./Datasets/SQL/Ingredients.csv')

    if not DatasetIngredients_Aux.exists():
        ProcessTabularData(DatasetIngredients_Aux)

    if not DatasetIngredients.exists():
        DataFrameIngredients_List = []
        for index , batch_ingredients in enumerate(ProcessEmbeddingsData(DatasetIngredients_Aux)):
            try:
                DumpDataFrameToSQL(batch_ingredients,'INGREDIENTS')
            except IntegrityError:
                MainLogger.info(f'Ingredients {index} Data Preloaded')
            DataFrameIngredients_List.append(batch_ingredients)
        
        DataFrameIngredients = pd.concat(DataFrameIngredients_List,ignore_index=True)
        DataFrameIngredients.to_csv(DatasetIngredients,index=False)
    
    else:
        BatchIngredientsDataFrame = pd.read_csv(DatasetIngredients,chunksize=250)
        for index , batch_data in enumerate(BatchIngredientsDataFrame):
            try:
                DumpDataFrameToSQL(batch_data,'INGREDIENTS')
            except IntegrityError:
                MainLogger.info(f'Ingredients Embeddings {index} Data Preloaded')