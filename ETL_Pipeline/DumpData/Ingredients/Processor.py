from uuid import uuid4
import pandas as pd
from joblib import Parallel , delayed , cpu_count
from functools import partial

from .Cleaner import CleanIngredientJSON , CleanIngredientsCSV
from ..Utils import InitSemanticModel
from ...Utils import GatherIngredientsNutritional_JSON , GatherIngredientsNutritional_CSV

NotNullColumns = [
    'Name',
    'Calories',
]
def ProcessData(DatasetIngredients):
    IngredientsJSONRaw = []
    for ingredient in GatherIngredientsNutritional_JSON():
        clean_ingredient = CleanIngredientJSON(ingredient)
        IngredientsJSONRaw.append(clean_ingredient)

    IngredientsCSV = GatherIngredientsNutritional_CSV()

    IngredientsCSVDataFrame = CleanIngredientsCSV(IngredientsCSV)
    IngredientsJSONDataFrame = pd.DataFrame(IngredientsJSONRaw,columns=IngredientsCSVDataFrame.columns)

    IngredientsDataFrame = pd.concat([IngredientsJSONDataFrame,IngredientsCSVDataFrame],ignore_index=True)
    IngredientsDataFrame.dropna(subset=NotNullColumns,inplace=True)
    IngredientsDataFrame['id'] = IngredientsDataFrame['Name'].apply(lambda value: uuid4())

    IngredientsDataFrame.to_csv(DatasetIngredients,index=False)
    return IngredientsDataFrame

def ProcessEmbeddingsData(DatasetIngredients):
    SemanticModel = InitSemanticModel()

    BatchIngredientsDataFrame = pd.read_csv(
        DatasetIngredients,
        usecols = ['Name','id'],
        chunksize = 250,
    )

    for batch_data in BatchIngredientsDataFrame:
        IngredientsEmbeddings = batch_data[['id']].copy()
        IngredientsEmbeddings['Embedding'] = SemanticModel.encode(batch_data['Name'].to_list()).tolist()
        yield IngredientsEmbeddings