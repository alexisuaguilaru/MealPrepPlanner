from pathlib import Path
import pandas as pd

from .Processor import ProcessData
from ..Utils import DumpDataFrameToSQL

def MainDumpIngredients():
    DatasetIngredients = Path('./Datasets/SQL/Ingredients.csv')

    if not DatasetIngredients.exists():
        IngredientsDataFrame = ProcessData(DatasetIngredients)
    else:
        IngredientsDataFrame = pd.read_csv(DatasetIngredients)

    NumRows = DumpDataFrameToSQL(IngredientsDataFrame,'INGREDIENTS')
    return NumRows