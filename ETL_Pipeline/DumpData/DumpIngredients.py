import re
from uuid import uuid4
import pandas as pd

from ..Utils import GatherIngredientsNutritional_JSON , GatherIngredientsNutritional_CSV

NotNullColumns = [
    'Name',
    'Calories',
]
def MainDumpIngredients():
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

    IngredientsDataFrame.to_csv('./Datasets/SQL/Ingredients.csv',index=False)
    return IngredientsDataFrame

def CleanFieldName(Ingredient):
    Name = Ingredient.get('Spanish Name') or Ingredient.get('English Name')
    return Name.capitalize() if Name else None

def CleanFieldsMacronutrients(Ingredient):
    return _ExtractCalories(Ingredient) , *_ExtractMacroValue(Ingredient)

def _ExtractMacroValue(Ingredient):
    Carbohydrates = 0
    Proteins = 0
    Fats = 0

    for nutrient in Ingredient['Nutrients']:
        if 'carbohidrato' in nutrient['Nutrient']:
            Carbohydrates = _CleanMacroValue(nutrient['Value'])
        if 'proteina' in nutrient['Nutrient']:
            Proteins = _CleanMacroValue(nutrient['Value'])
        if 'grasa' in nutrient['Nutrient']: 
            Fats = _CleanMacroValue(nutrient['Value'])

    return Carbohydrates , Proteins , Fats

def _ExtractCalories(Ingredient):
    Calories = Ingredient.get('Calories')
    return int(Calories) if Calories else None

MacroValuePattern = r'\d+'
def _CleanMacroValue(MacronutrientValue):
    MacroValueMatch = re.search(MacroValuePattern,MacronutrientValue)
    try:
        return int(MacroValueMatch[0])
    except TypeError:
        return 0
    
def CleanIngredientsCSV(Ingredients):
    CleanIngredients = Ingredients[['nombre_del_alimento','energ_kcal','carbohydrt','protein','lipid_tot']].copy()
    CleanIngredients.rename(
        columns = {
            'nombre_del_alimento': 'Name',
            'energ_kcal': 'Calories',
            'carbohydrt': 'Carbohydrates',
            'protein': 'Proteins',
            'lipid_tot': 'Fats',
        }, 
        inplace = True
    )

    Macronutrients = ['Calories','Carbohydrates','Proteins','Fats']
    CleanIngredients['Name'] = CleanIngredients['Name'].apply(str.capitalize)
    CleanIngredients[Macronutrients] = CleanIngredients[Macronutrients].astype(int)

    return CleanIngredients

FieldCleanersPipeline = [
    CleanFieldName,
]
def CleanIngredientJSON(Ingredient):
    CleanFields = [field_cleaner(Ingredient) for field_cleaner in FieldCleanersPipeline]
    CleanFields.extend(CleanFieldsMacronutrients(Ingredient))
    return CleanFields