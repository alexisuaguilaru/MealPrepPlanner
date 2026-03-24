from pathlib import Path
import asyncio

from .ScrapeMealtimes import MainScrapeMealtimes
from .ScrapeRecipes import MainScrapeRecipesMealtime
from .ScrapeRecipeInfo import MainScrapeRecipeInformation
from ...Utils import SaveCleanRecipeInfo

def MainScraping():
    RecipesPath = Path('Datasets/Recipes/EatRight/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    BaseURL_EatRight = 'https://www.eatright.org'
    
    Mealtimes = asyncio.run(MainScrapeMealtimes())
    for mealtime in Mealtimes[:1]:
        mealtime_link = BaseURL_EatRight + mealtime['Link']
        for recipe in asyncio.run(MainScrapeRecipesMealtime(mealtime_link))[:4]:
            recipe_link = BaseURL_EatRight + recipe['Link']
            recipe_info = asyncio.run(MainScrapeRecipeInformation(recipe_link))

    return []