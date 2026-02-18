import asyncio

from .ScrapeRecipes import MainScrapRecipesFromCuisine
from .ScrapeRecipesInfo import MainScrapRecipeInformation

def MainScrapping():
    MexicanRecipes = asyncio.run(MainScrapRecipesFromCuisine('https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/'))
    return MexicanRecipes