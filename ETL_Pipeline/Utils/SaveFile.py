import re
import json

def SaveCleanRecipeInfo(RecipeInfo,RecipesPath):
    recipe_name = re.sub(r'\s+','',RecipeInfo['Name'].title())
    path_json = RecipesPath/f'{recipe_name}.json'

    with open(path_json,'w',encoding='utf-8') as file_json:
        json.dump(RecipeInfo,file_json,ensure_ascii=False,indent=4)
        
    return path_json