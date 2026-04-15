from pathlib import Path
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessRelations_RecipesPrices
from ...Database import CreateConnectionToSQL 
from ...Database.Connector import SCHEMA_DB

def MainDumpRecipesPrices(MainLogger):
    DatasetRecipesPrices = Path('./Datasets/SQL/RecipesPrices.csv')

    if not DatasetRecipesPrices.exists():
        DataFrameRecipesPrices = ProcessRelations_RecipesPrices()
        DataFrameRecipesPrices.to_csv(DatasetRecipesPrices,index=False)

    else:
        DataFrameRecipesPrices = pd.read_csv(DatasetRecipesPrices)

    with CreateConnectionToSQL().begin() as ConnectionToSQL:
        for _id , _price_serving in DataFrameRecipesPrices.iloc:
            try:
                update_query = text(f"""UPDATE "{SCHEMA_DB}"."RECIPES" SET "PricePerServing"={_price_serving} WHERE id='{_id}';""")
                ConnectionToSQL.execute(update_query)
            except IntegrityError:
                MainLogger.info(f'Recipe {_id} Price Preloaded')