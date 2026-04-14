from pathlib import Path
import pandas as pd 
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessData
from ..Utils import DumpDataFrameToSQL

def MainDumpIngredients_Prices(MainLogger):
    DatasetIngredientsPrices = Path('./Datasets/SQL/IngredientsPrices.csv')

    if not DatasetIngredientsPrices.exists():
        IngredientsPricesDataFrame_List = []
        for index , batch_ingredients_prices in enumerate(ProcessData()):
            try: 
                DumpDataFrameToSQL(batch_ingredients_prices,'INGREDIENTS_PRICES')
            except IntegrityError:
                MainLogger.info(f'Ingredients_Prices Relations {index} Data Preloaded')
            IngredientsPricesDataFrame_List.append(batch_ingredients_prices)
        
        IngredientsPricesDataFrame = pd.concat(IngredientsPricesDataFrame_List,ignore_index=True)
        IngredientsPricesDataFrame.to_csv(DatasetIngredientsPrices,index=False)
    else:
        BatchIngredientsPricesDataFrame = pd.read_csv(DatasetIngredientsPrices,chunksize=250)
        for index , batch_ingredients_prices in enumerate(BatchIngredientsPricesDataFrame):
            try:
                DumpDataFrameToSQL(batch_ingredients_prices,'INGREDIENTS_PRICES')
            except IntegrityError:
                MainLogger.info(f'Recipes_Ingredients Relations {index} Data Preloaded')