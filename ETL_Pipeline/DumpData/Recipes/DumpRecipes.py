from pathlib import Path
import pandas as pd
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessData
from ..Utils import DumpDataFrameToSQL

def MainDumpRecipes(MainLogger):
    DatasetRecipes = Path('./Datasets/SQL/Recipes.csv')
    
    if not DatasetRecipes.exists():
        RecipesDataFrame = ProcessData(DatasetRecipes)
    else:
        RecipesDataFrame = pd.read_csv(DatasetRecipes)
    
    try:
        DumpDataFrameToSQL(RecipesDataFrame,'RECIPES')
    except IntegrityError:
        MainLogger.info('Recipes Data Preloaded')