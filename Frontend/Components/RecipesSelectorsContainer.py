import streamlit as st

from Utils import GetRecipesRecommendations

DaysLabels = ['Lunes','Martes','Miércoles','Jueves','Viernes']
MealsLabels = ['Desayuno','Almuerzo','Comida']
def RecipesSelectors():
    SelectedRecipes = st.session_state.get('SelectedRecipes',{})
    DaysColumns = st.columns(6)

    with DaysColumns[0]:
        with st.container():
            with _AddContentBlock(False):
                pass

            for meal in MealsLabels:
                with _AddContentBlock():
                    st.markdown(f'**:green[{meal}]**',text_alignment='center')

    for day , day_column in zip(DaysLabels,DaysColumns[1:]):
        with day_column:
            with st.container():
                with _AddContentBlock():
                    st.markdown(f'**:green[{day}]**',text_alignment='center')

                for meal in MealsLabels:
                    recipe_key = f'{day}_{meal}'
                    recipe = SelectedRecipes.get(recipe_key)

                    with _AddContentBlock(False):
                        if not recipe:
                            if _AddRecipeSelector(recipe_key):
                                _RecipeSelectorDialog(recipe_key)
                        else:
                            if _AddMinimalRecipe(recipe_key):
                                _ModificationSelectedRecipe(recipe_key)

def _AddContentBlock(
        Border = True,
        Height = 85,
    ):
    return st.container(border=Border,height=Height,vertical_alignment='center',horizontal_alignment='center')

def _AddRecipeSelector(RecipeKey):
    return st.button(
            ':small[Seleccionar una receta]', 
            key = f'select_{RecipeKey}',
            use_container_width = True,
        )

def _AddMinimalRecipe(RecipeKey):
    Recipe = st.session_state['SelectedRecipes'][RecipeKey]
    return st.button(
            _FormatRecipeName(Recipe['Name']),
            key = f'info_{RecipeKey}',
            use_container_width = True,
        )

@st.dialog('Seleccione una receta',width='medium')
def _RecipeSelectorDialog(DayMealKey):
    PrevRecipesID = [recipe['id'] for recipe in st.session_state['SelectedRecipes'].values()]
    Recommendations = GetRecipesRecommendations(PrevRecipesID)

    GridRecipes = st.columns(2)
    for index , recipe in enumerate(Recommendations[:30]):
        with GridRecipes[index%2]:
            with _AddContentBlock(Height=650):
                _AddRecipeCard(DayMealKey,recipe)

@st.dialog('Modificar receta seleccionada',width='small')
def _ModificationSelectedRecipe(DayMealKey):
    Recipe = st.session_state['SelectedRecipes'][DayMealKey]
    with _AddContentBlock(False,Height=360):
        st.markdown(f"**{Recipe['Name']}**",text_alignment='center')
        st.image(Recipe['Image'],width=240)
        if st.button(
                'Eliminar receta',
                use_container_width = True,
            ):
            del st.session_state['SelectedRecipes'][DayMealKey]
            st.rerun()            

NutrientLabels = ['Calories','Carbohydrates','Proteins','Fats']
NutrientNames = ['calorías','carbohidratos','proteínas','grasas']
def _AddRecipeCard(DayMealKey,Recipe):
    if st.button(
        Recipe['Name'],
        key = f"{DayMealKey}_{Recipe['id']}",
        use_container_width = True
    ):
        st.session_state['SelectedRecipes'][DayMealKey] = Recipe
        st.rerun()

    st.image(Recipe['Image'],width=240)

    st.divider()

    NutrientsColumns = st.columns(2)
    for index , (nutrient , name) in enumerate(zip(NutrientLabels,NutrientNames)):
        with NutrientsColumns[index%2]:
            st.markdown(f'{Recipe[nutrient]} {name}',text_alignment='center')

    with NutrientsColumns[0]:
        with st.container(horizontal_alignment='center'):
            with st.popover('Instrucciones'):
                st.markdown('**Instrucciones**',text_alignment='center')
                st.markdown(Recipe['Instructions'])

    with NutrientsColumns[1]:
        with st.container(horizontal_alignment='center'):
            with st.popover('Ingredientes'):
                st.markdown('**Ingredientes**',text_alignment='center')
                for ingredient in Recipe['RECIPES_INGREDIENTS']:
                    amount = ingredient['StringAmount'] or ''
                    unit = ingredient['UnitMeasurement'] or ''
                    name = ingredient['IngredientName'] or ''
                    ingredient_info = ' '.join([amount,unit,name])
                    st.markdown('* '+ingredient_info)
        
    st.divider()

    with st.container(horizontal_alignment='center',vertical_alignment='center'):
        st.markdown(f"{Recipe['Servings']} porciones con costo de ${Recipe['PricePerServing']:.2f} por porción",text_alignment='center')

def _FormatRecipeName(
        RecipeName,
        Limit = 20,
    ):
    if Limit < len(RecipeName):
        RecipeName = RecipeName[:Limit]+'...'
    return f'**:small[{RecipeName}]**'