from pathlib import Path
import asyncio

from .ScrapeMealtimes import MainScrapeMealtimes
from ...Utils import SaveCleanRecipeInfo

def MainScraping():
    RecipesPath = Path('Datasets/Recipes/EatRight/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    Mealtimes = asyncio.run(MainScrapeMealtimes())
    for mealtime in Mealtimes:
        mealtime_link = 'https://www.eatright.org' + mealtime['Link']

    return asyncio.run(MainScrapeMealtimes())