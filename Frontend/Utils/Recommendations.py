from uuid import UUID

from .Connection import ConnectionToAPI

ColumnsRecipes = ['id','Name','Calories','Carbohydrates','Proteins','Fats','Image','Instructions','Servings','PricePerServing']
ColumnsIngredients = 'RECIPES_INGREDIENTS(StringAmount,IngredientName,UnitMeasurement,ingredient_id)'
def GetRecipesRecommendations(
        PrevRecipesID: list[UUID] = [],
    ):
    
    BaseSelectRecommendations = (
    ConnectionToAPI
        .from_('RECIPES')
        .select(
            *ColumnsRecipes,
            ColumnsIngredients,
        )
        .filter('id','not.in',f"({','.join(PrevRecipesID)})")
        .gt('PricePerServing',0)
    )

    if not PrevRecipesID: 
        return (
        BaseSelectRecommendations
            .execute()
        ).data
    
    else:
        FilteredRecipesID = _GetFilteredRecipes(PrevRecipesID)

        return (
        BaseSelectRecommendations
            .in_('id',FilteredRecipesID)
            .execute()
        ).data
    
def _GetFilteredRecipes(
        PrevRecipesID: list[UUID],
    ):

    QueryPrevSelectedIngredients = (
    ConnectionToAPI
        .from_('RECIPES')
        .select('RECIPES_INGREDIENTS(ingredient_id)')
        .filter('id','in',f"({','.join(PrevRecipesID)})")
        .execute()
    ).data

    PrevSelectedIngredients = {
        ingredient['ingredient_id'] 
        for recipe_ingredienst in QueryPrevSelectedIngredients 
            for ingredient in recipe_ingredienst['RECIPES_INGREDIENTS']
    }

    FilteredRecipesID = (
    ConnectionToAPI
        .from_('RECIPES_INGREDIENTS')
        .select('recipe_id')
        .in_('ingredient_id',PrevSelectedIngredients)
        .execute()
    ).data

    return {recipe['recipe_id'] for recipe in FilteredRecipesID}