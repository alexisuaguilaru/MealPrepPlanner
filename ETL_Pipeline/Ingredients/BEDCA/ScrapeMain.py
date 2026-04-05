from pathlib import Path
import asyncio

from .ScrapeIngredients import MainScrapeIngredients
from .ScrapeNutritionalFacts import MainScrapeIngredientNutritionalFacts
from .CleanIngredientInfo import CleanNutritionalFacts
from .SaveIngredient import SaveCleanIngredient

from ...Utils import ResumeDownloading

def MainScraping():
    DatasetPath = Path('Datasets/IngredientsNutritional/BEDCA/')
    DatasetPath.mkdir(parents=True,exist_ok=True)

    TotalIngredients , LastIngredient = ResumeDownloading(DatasetPath)
    
    Ingredients = asyncio.run(MainScrapeIngredients())
    for ingredient in Ingredients[TotalIngredients:]:
        clean_ingredient_info = {
            'Spanish Name': ingredient['Spanish Name'],
            'English Name': ingredient['English Name'],
        }

        nutritional_facts = asyncio.run(MainScrapeIngredientNutritionalFacts(ingredient['Ingredient ID']))
        clean_calories , clean_nutritional_facts = CleanNutritionalFacts(nutritional_facts)
        clean_ingredient_info['Calories'] = clean_calories
        clean_ingredient_info['Nutrients'] = clean_nutritional_facts

        yield SaveCleanIngredient(clean_ingredient_info,DatasetPath)