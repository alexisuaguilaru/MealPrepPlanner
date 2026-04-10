from uuid import uuid4
import pandas as pd

from ...Utils import GatherIngredientsNutritional_JSON , GatherIngredientsNutritional_CSV
from .Cleaner import CleanIngredientJSON , CleanIngredientsCSV

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