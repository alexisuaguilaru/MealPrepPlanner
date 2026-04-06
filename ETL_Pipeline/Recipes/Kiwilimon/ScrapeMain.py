from pathlib import Path
import asyncio
import re

from .Login import PerformLogin
from .ScrapeRecipes import MainScrapeRecipesFromPage
from .ScrapeRecipeInfo import MainScrapeRecipeInformation
from .CleanRecipeInfo import CleanRecipe

from ...Utils import SaveCleanRecipeInfo , ResumeDownloading

def MainScraping(NumClicks: int = 1):
    RecipesPath = Path('Datasets/Recipes/Kiwilimon/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    asyncio.run(PerformLogin())

    RecipesList = asyncio.run(MainScrapeRecipesFromPage(NumClicks))
    TotalRecipes , LastRecipe = ResumeDownloading(RecipesPath)

    for recipe in RecipesList[TotalRecipes:]:
        recipe_link = 'https://www.kiwilimon.com'+recipe['Link']
        recipe_info = asyncio.run(MainScrapeRecipeInformation(recipe_link))

        clean_recipe_info = CleanRecipe(recipe_info)
        clean_recipe_info['Name'] = re.sub(r'[¿?"]*','',recipe['Recipe Name'])
        clean_recipe_info['Image'] = recipe['Recipe Image']
        clean_recipe_info['Source'] = recipe_link

        yield SaveCleanRecipeInfo(clean_recipe_info,RecipesPath)