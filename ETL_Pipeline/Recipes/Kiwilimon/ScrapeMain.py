from pathlib import Path
import asyncio

from .Login import PerformLogin
from .ScrapeRecipes import MainScrapeRecipesFromPage
from .ScrapeRecipeInfo import MainScrapeRecipeInformation

def MainScraping(NumClicks: int = 1):
    RecipesPath = Path('Datasets/Recipes/Kiwilimon/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    # asyncio.run(PerformLogin())

    # RecipesList = asyncio.run(MainScrapeRecipesFromPage(NumClicks))
    RecipesList = [{'Link': '/receta/recetas-faciles/caldo-de-queso'}]

    RecipesInfo = []
    for recipe in RecipesList[:4]:
        recipe_info = asyncio.run(MainScrapeRecipeInformation('https://www.kiwilimon.com'+recipe['Link']))
        RecipesInfo.append(recipe_info)

    return RecipesInfo