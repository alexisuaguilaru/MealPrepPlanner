from dataclasses import dataclass
from uuid import UUID

from .Connection import ConnectionToAPI

@dataclass
class GeneralRecipesInformation:
    Calories: float = 0
    Carbohydrates: float = 0
    Proteins: float = 0
    Fats: float = 0
    PricePerServing: float = 0

ColumnsRecipes = ['Calories','Carbohydrates','Proteins','Fats','PricePerServing']
def GetGeneralRecipesInformation(
        SelectedRecipesID: list[UUID],
    ) -> GeneralRecipesInformation:

    RecipesInformation = GeneralRecipesInformation()
    NumberRecipes = len(SelectedRecipesID)

    if SelectedRecipesID:
        Recipes = (
        ConnectionToAPI
            .from_('RECIPES')
            .select(
                *ColumnsRecipes,
            )
            .in_('id',SelectedRecipesID)
            .execute()
        ).data

        for recipe in Recipes:
            RecipesInformation.Calories += recipe['Calories']/NumberRecipes
            RecipesInformation.Carbohydrates += recipe['Carbohydrates']/NumberRecipes
            RecipesInformation.Proteins += recipe['Proteins']/NumberRecipes
            RecipesInformation.Fats += recipe['Fats']/NumberRecipes
            RecipesInformation.PricePerServing += recipe['PricePerServing']/NumberRecipes

    return RecipesInformation