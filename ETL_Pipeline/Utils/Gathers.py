from pathlib import Path
import json
import pandas as pd

def GatherRecipes():
    RecipesDataset = Path('./Datasets/Recipes')
    for recipe_json in RecipesDataset.glob('**/*.json'):
        with open(recipe_json,'r',encoding='utf-8') as json_file:
            yield json.load(json_file)

def GatherIngredientsNutritional_JSON():
    IngredientsDataset = Path('./Datasets/IngredientsNutritional')
    for ingredient_json in IngredientsDataset.glob('**/*.json'):
        with open(ingredient_json,'r',encoding='utf-8') as json_file:
            yield json.load(json_file)

def GatherIngredientsNutritional_CSV():
    IngredientsDataset = Path('./Datasets/IngredientsNutritional')
    INSPDataset = IngredientsDataset/'INSP'/'clean.csv'
    return pd.read_csv(INSPDataset)