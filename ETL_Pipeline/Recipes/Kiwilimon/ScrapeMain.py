from pathlib import Path
import asyncio

from .ScrapeRecipes import MainScrapeRecipesFromPage
from .Login import PerformLogin

def MainScraping(NumClicks: int = 2):
    RecipesPath = Path('Datasets/Recipes/Kiwilimon/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    asyncio.run(PerformLogin())
    
    RecipesList = asyncio.run(MainScrapeRecipesFromPage(NumClicks))

    return RecipesList