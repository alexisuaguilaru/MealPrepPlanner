import asyncio

from .ScrapeRecipes import MainScrapeRecipesFromCuisine
from .ScrapeRecipesInfo import MainScrapeRecipeInformation
from .CleanRecipeInfo import CleanRecipe

def MainScraping():
    MexicanRecipes = asyncio.run(MainScrapeRecipesFromCuisine('https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/'))
    for mexican_recipe in MexicanRecipes[5:6]:
        recipe_name:str = mexican_recipe['Recipe Name']
        recipe_link = mexican_recipe['Link']
        recipe_info = asyncio.run(MainScrapeRecipeInformation(recipe_link))

        if not any([] == info for info in recipe_info):
            clean_recipe_info = CleanRecipe(recipe_info)
            clean_recipe_info['Name'] = recipe_name
            clean_recipe_info['Source'] = recipe_link
            yield clean_recipe_info