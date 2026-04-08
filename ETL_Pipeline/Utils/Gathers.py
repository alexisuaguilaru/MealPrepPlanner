from pathlib import Path
import json

def GatherRecipes():
    RecipesDataset = Path('./Datasets/Recipes')
    for recipe_json in RecipesDataset.glob('**/*.json'):
        with open(recipe_json,'r',encoding='utf-8') as json_file:
            yield json.load(json_file)