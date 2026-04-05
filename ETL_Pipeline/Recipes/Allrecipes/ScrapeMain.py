from pathlib import Path
import asyncio

from .ScrapeRecipes import MainScrapeRecipesFromCuisine
from .ScrapeRecipesInfo import MainScrapeRecipeInformation
from .CleanRecipeInfo import CleanRecipe

from ...Utils import SaveCleanRecipeInfo , ResumeDownloading

def MainScraping():
    RecipesPath = Path('Datasets/Recipes/Allrecipes/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    MexicanRecipes = asyncio.run(MainScrapeRecipesFromCuisine('https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/'))
    TotalRecipes , LastRecipe = ResumeDownloading(RecipesPath)

    for mexican_recipe in MexicanRecipes[TotalRecipes+4:]:
        recipe_name:str = mexican_recipe['Recipe Name']
        recipe_link = mexican_recipe['Link']
        recipe_info = asyncio.run(MainScrapeRecipeInformation(recipe_link))

        if not any([] == info for info in recipe_info):
            clean_recipe_info = CleanRecipe(recipe_info)
            clean_recipe_info['Name'] = recipe_name
            clean_recipe_info['Source'] = recipe_link
            yield SaveCleanRecipeInfo(clean_recipe_info,RecipesPath)