import asyncio

from .ScrapeRecipes import MainScrapRecipesFromCuisine
from .ScrapeRecipesInfo import MainScrapRecipeInformation
from .CleanRecipeInfo import *

def MainScrapping():
    MexicanRecipes = asyncio.run(MainScrapRecipesFromCuisine('https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/'))
    for mexican_recipe in MexicanRecipes[:10]:
        recipe_name:str = mexican_recipe['Recipe_Name']
        recipe_link = mexican_recipe['Link']
        recipe_info = asyncio.run(MainScrapRecipeInformation(recipe_link))

        if not any([] == info for info in recipe_info):
            print(recipe_name.upper())
            print(recipe_info)