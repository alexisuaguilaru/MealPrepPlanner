from pathlib import Path
import asyncio
import re

from .ScrapeMealtimes import MainScrapeMealtimes
from .ScrapeRecipes import MainScrapeRecipesMealtime
from .ScrapeRecipeInfo import MainScrapeRecipeInformation
from .CleanRecipeInfo import CleanRecipe

from ...Utils import SaveCleanRecipeInfo , ResumeDownloading

def MainScraping():
    RecipesPath = Path('Datasets/Recipes/EatRight/')
    RecipesPath.mkdir(parents=True,exist_ok=True)

    BaseURL_EatRight = 'https://www.eatright.org'

    Mealtimes = asyncio.run(MainScrapeMealtimes())
    TotalMealtimes , LastMealtime = ResumeDownloading(RecipesPath)

    for mealtime in Mealtimes[TotalMealtimes:-1]:
        mealtime_link = BaseURL_EatRight + mealtime['Link']
        MealtimePath = RecipesPath/(mealtime['Mealtime'].title().replace(' ',''))
        MealtimePath.mkdir(parents=True,exist_ok=True)

        Recipes = asyncio.run(MainScrapeRecipesMealtime(mealtime_link))
        TotalRecipes , LastRecipe = ResumeDownloading(MealtimePath)

        for recipe in Recipes[TotalRecipes:len(Recipes)//2]:
            recipe_link = BaseURL_EatRight + recipe['Link']
            recipe_info = asyncio.run(MainScrapeRecipeInformation(recipe_link))

            if (recipe_info!={}) or recipe_info.get('Servings Nutritional Facts',None) or recipe_info.get('Ingredients',None):
                clean_recipe_info = CleanRecipe(recipe_info)
            else:
                clean_recipe_info = {}
            clean_recipe_info['Name'] = re.sub(r'([Rr]ecipe|")','',recipe['Recipe Name']).strip()
            clean_recipe_info['Image'] = BaseURL_EatRight + recipe['Recipe Image']
            clean_recipe_info['Source'] = recipe_link

            yield SaveCleanRecipeInfo(clean_recipe_info,MealtimePath)