from pathlib import Path
import asyncio
import re

from .ScrapeMealtimes import MainScrapeMealtimes
from .ScrapeRecipes import MainScrapeRecipesMealtime
from .ScrapeRecipeInfo import MainScrapeRecipeInformation
from .CleanRecipeInfo import CleanRecipe
from ...Utils import SaveCleanRecipeInfo

def MainScraping():
    RecipesPath = Path('Datasets/Recipes/EatRight/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    BaseURL_EatRight = 'https://www.eatright.org'

    Mealtimes = asyncio.run(MainScrapeMealtimes())
    for mealtime in Mealtimes:
        mealtime_link = BaseURL_EatRight + mealtime['Link']
        for recipe in asyncio.run(MainScrapeRecipesMealtime(mealtime_link)):
            recipe_link = BaseURL_EatRight + recipe['Link']
            recipe_info = asyncio.run(MainScrapeRecipeInformation(recipe_link))

            clean_recipe_info = CleanRecipe(recipe_info)
            clean_recipe_info['Name'] = re.sub(r'[Rr]ecipe','',recipe['Recipe Name']).strip()
            clean_recipe_info['Image'] = BaseURL_EatRight + recipe['Recipe Image']
            clean_recipe_info['Source'] = recipe_link

            yield SaveCleanRecipeInfo(clean_recipe_info,RecipesPath)