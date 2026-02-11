import asyncio
from ETL_Pipeline import MainScrapCuisines , MainScrapRecipesFromCuisine , MainScrapRecipeInformation

if __name__ == "__main__":

    for cuisine_representation in asyncio.run(MainScrapCuisines()):
        cuisine_name = cuisine_representation['Cuisine']
        cuisine_link = cuisine_representation['Link']

        for recipe_representation in asyncio.run(MainScrapRecipesFromCuisine(cuisine_link)):
            recipe_name = recipe_representation['Recipe_Name']
            recipe_link = recipe_representation['Link']

            asyncio.run(MainScrapRecipeInformation(recipe_link))