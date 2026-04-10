import re

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

def CleanIngredientJSON(Ingredient):
    CleanFields = [field_cleaner(Ingredient) for field_cleaner in FieldCleanersPipeline]
    CleanFields.extend(CleanFieldsMacronutrients(Ingredient))
    return CleanFields

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

FieldCleanersPipeline = [
    CleanFieldName,
]