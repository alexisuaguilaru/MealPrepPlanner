import asyncio

from .ScrapeIngredients import MainScrapeIngredients

def MainScraping():
    IngredientsNutritionalFacts = asyncio.run(MainScrapeIngredients())
    return IngredientsNutritionalFacts