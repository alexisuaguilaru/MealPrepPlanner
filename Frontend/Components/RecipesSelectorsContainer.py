import streamlit as st

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
                            _AddRecipeSelector(recipe_key)

def _AddContentBlock(Border=True):
    return st.container(border=Border,height=85,vertical_alignment='center',horizontal_alignment='center')

def _AddRecipeSelector(RecipeKey):
    return st.button(
            ':small[Seleccionar una receta]', 
            key = f'select_{RecipeKey}',
            use_container_width = True,
        )