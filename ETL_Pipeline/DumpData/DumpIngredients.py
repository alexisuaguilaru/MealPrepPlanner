import re

from ..Utils import GatherIngredientsNutritional_JSON , GatherIngredientsNutritional_CSV

def MainDumpIngredients():
    for ingredient in GatherIngredientsNutritional_JSON():
        CleanIngredientJSON(ingredient)

    IngredientsCSV = GatherIngredientsNutritional_CSV()
    IngredientsCSV = CleanIngredientsCSV(IngredientsCSV)

FieldCleanersPipeline = [
    CleanFieldName,
]
def CleanIngredientJSON(Ingredient):
    CleanFields = [field_cleaner(Ingredient) for field_cleaner in FieldCleanersPipeline]
    CleanFields.extend(CleanFieldsMacronutrients(Ingredient))
    return CleanFields

def CleanFieldName(Ingredient):
    Name = Ingredient.get('Spanish Name') or Ingredient.get('English Name')
    return Name.capitalize()

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
    return int(Ingredient['Calories'])

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