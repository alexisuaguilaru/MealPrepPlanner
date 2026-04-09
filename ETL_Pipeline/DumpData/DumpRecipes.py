import re
from uuid import uuid4
import pandas as pd

from ..Utils import GatherRecipes

ColumnsRecipe = [
    'Name',
    'TotalTime',
    'Servings',
    'Instructions',
    'Image',
    'Source',
    'Calories',
    'Carbohydrates',
    'Proteins',
    'Fats',
]
NotNullColumns = [
    'Name',
    'TotalTime',
    'Servings',
    'Instructions',
    'Source',
]
def MainDumpRecipes():
    RecipesRaw = []
    for recipe in GatherRecipes():
        clean_recipe = CleanFieldsRecipe(recipe)
        RecipesRaw.append(clean_recipe)

    RecipesDataFrame = pd.DataFrame(RecipesRaw,columns=ColumnsRecipe)
    RecipesDataFrame.dropna(subset=NotNullColumns,inplace=True)
    RecipesDataFrame['id'] = RecipesDataFrame['Name'].apply(lambda value: uuid4())
    RecipesDataFrame.dropna(subset=NotNullColumns,inplace=True)

    RecipesDataFrame.to_csv('./Datasets/SQL/Recipes.csv',index=False)
    return RecipesDataFrame

def CleanFieldName(Recipe):
    Name = Recipe.get('Name')
    return Name.capitalize() if Name else None

TimePattern = r'((?P<hours>\d+)\s*hrs?)?\s*((?P<minutes>\d+)\s*mins?)?'
def CleanFieldTotalTime(Recipe):
    StrTime = Recipe.get('Total Time','0 mins')
    TimeMatch = re.search(TimePattern,StrTime)
    Hours = TimeMatch.groupdict().get('hours') or 0
    Minutes = TimeMatch.groupdict().get('minutes') or 0
    return int(Hours)*60 + int(Minutes)

ServingsPattern = r'\d+'
def CleanFieldServings(Recipe):
    StrServings = Recipe.get('Servings',1)
    if isinstance(StrServings,str):
        ServingsMatch = re.search(ServingsPattern,StrServings)
        Servings = int(ServingsMatch[0])
    else:
        Servings = StrServings
    return Servings

def CleanFieldInstructions(Recipe):
    ListSteps = Recipe.get('Instructions')
    Instructions = None
    if ListSteps:
        EnumeratedSteps = enumerate(ListSteps,1)
        Instructions = '\n'.join(map(_FormatInstructionStep,EnumeratedSteps))        
    return Instructions

def CleanFieldImage(Recipe):
    return Recipe.get('Image','')

def CleanFieldSource(Recipe):
    return Recipe.get('Source','')

def _FormatInstructionStep(InstructionStep):
    return '{}. {}'.format(*InstructionStep)

def CleanFieldsMacronutrients(Recipe):
    NutritionalFacts = Recipe.get('NutritionalFacts')
    Calories = None
    Carbohydrates = None
    Proteins = None
    Fats = None
    
    if NutritionalFacts:
        Calories = NutritionalFacts.get('Calories')
        Calories = _ExtractMacroValue(Calories)

        Carbohydrates = NutritionalFacts.get('Carbohydrate') or NutritionalFacts.get('Total Carbohydrate')
        Carbohydrates = _ExtractMacroValue(Carbohydrates)

        Proteins = NutritionalFacts.get('Protein')
        Proteins = _ExtractMacroValue(Proteins)

        Fats = NutritionalFacts.get('Total Fat')
        Fats = _ExtractMacroValue(Fats)
    
    return Calories , Carbohydrates , Proteins , Fats

def _ExtractMacroValue(Macronutrient):
    if not Macronutrient: return None
    MatchMacronutrient = re.search(r'\d+',Macronutrient)
    return int(MatchMacronutrient[0]) if MatchMacronutrient else None

FieldCleanersPipeline = [
    CleanFieldName,
    CleanFieldTotalTime,
    CleanFieldServings,
    CleanFieldInstructions,
    CleanFieldImage,
    CleanFieldSource,
]
def CleanFieldsRecipe(Recipe):
    CleanFields = [field_cleaner(Recipe) for field_cleaner in FieldCleanersPipeline]
    CleanFields.extend(CleanFieldsMacronutrients(Recipe))
    return CleanFields