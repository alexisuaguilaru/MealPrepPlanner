import re
import json

from pathlib import Path

def SaveCleanRecipeInfo(RecipeInfo,RecipesPath:Path):
    recipe_name = re.sub(r'\s+','',RecipeInfo['Name'].title())
    path_json = RecipesPath/f'{recipe_name}.json'

    with open(path_json,'w',encoding='utf-8') as file_json:
        json.dump(RecipeInfo,file_json,ensure_ascii=False,indent=4)
        
    return path_json

def SaveMarkdownFile(MarkdownContent,FilePath:Path):
    with open(FilePath,'w',encoding='utf-8') as markdown_file:
        markdown_file.write(MarkdownContent)

def ResumeDownloading(DownloadsDir:Path):
    Files = list(DownloadsDir.iterdir())
    LastFile = Files[-1] if Files else None
    return len(Files) , LastFile