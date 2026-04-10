from pathlib import Path
import pandas as pd

from .Processor import ProcessData
from ..Utils import DumpDataFrameToSQL

def MainDumpRecipes():
    DatasetRecipes = Path('./Datasets/SQL/Recipes.csv')
    
    if not DatasetRecipes.exists():
        RecipesDataFrame = ProcessData(DatasetRecipes)
    else:
        RecipesDataFrame = pd.read_csv(DatasetRecipes)
    
    NumRows = DumpDataFrameToSQL(RecipesDataFrame,'RECIPES')
    return NumRows