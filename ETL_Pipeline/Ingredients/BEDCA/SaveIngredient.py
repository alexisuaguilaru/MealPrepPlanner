import re
import json

def SaveCleanIngredient(IngredientInfo,DatasetPath):
    spanish_name = re.sub(r"""[\s"'\\\/\(\)%><]+""",'',IngredientInfo['Spanish Name'].title())
    english_name = re.sub(r"""[\s"'\\\/\(\)%><]+""",'',IngredientInfo['English Name'].title())
    path_json = DatasetPath/f'{spanish_name}_{english_name}.json'

    with open(path_json,'w',encoding='utf-8') as file_json:
        json.dump(IngredientInfo,file_json,ensure_ascii=False,indent=4)
        
    return path_json