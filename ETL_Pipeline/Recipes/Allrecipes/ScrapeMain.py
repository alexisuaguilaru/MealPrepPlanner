import asyncio

from .ScrapeRecipes import MainScrapRecipesFromCuisine
from .ScrapeRecipesInfo import MainScrapRecipeInformation
from .CleanRecipeInfo import CleanRecipe

def MainScrapping():
    MexicanRecipes = asyncio.run(MainScrapRecipesFromCuisine('https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/'))
    for mexican_recipe in MexicanRecipes[:10]:
        recipe_name:str = mexican_recipe['Recipe Name']
        recipe_link = mexican_recipe['Link']
        recipe_info = asyncio.run(MainScrapRecipeInformation(recipe_link))

        if not any([] == info for info in recipe_info):
            clean_recipe_info = CleanRecipe(recipe_info)
            clean_recipe_info['Name'] = recipe_name
            print(clean_recipe_info)