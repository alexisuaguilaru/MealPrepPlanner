from pathlib import Path
import asyncio

from .ScrapeRecipes import MainScrapeRecipesFromPage

def MainScraping():
    RecipesPath = Path('Datasets/Recipes/Kiwilimon/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    RecipesList = asyncio.run(MainScrapeRecipesFromPage())
    return RecipesList