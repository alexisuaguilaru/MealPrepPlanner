import asyncio

from .ScrapeIngredients import MainScrapeIngredients
from .ScrapeNutritionalFacts import MainScrapeIngredientNutritionalFacts
from .CleanIngredientInfo import CleanNutritionalFacts

def MainScraping():
    Ingredients = asyncio.run(MainScrapeIngredients())
    for ingredient in Ingredients[:10]:
        clean_ingredient_info = {
            'Spanish Name': ingredient['Spanish Name'],
            'English Name': ingredient['English Name'],
        }

        nutritional_facts = asyncio.run(MainScrapeIngredientNutritionalFacts(ingredient['Ingredient ID']))
        clean_calories , clean_nutritional_facts = CleanNutritionalFacts(nutritional_facts)
        clean_ingredient_info['Calories'] = clean_calories
        clean_ingredient_info['Nutrients'] = clean_nutritional_facts

        yield clean_ingredient_info