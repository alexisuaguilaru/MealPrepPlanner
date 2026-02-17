import asyncio

from .ScrapeRecipes import MainScrapRecipesFromCuisine
from .ScrapeRecipesInfo import MainScrapRecipeInformation

async def MainScrapping():
    MexicanRecipes = MainScrapRecipesFromCuisine('https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/')