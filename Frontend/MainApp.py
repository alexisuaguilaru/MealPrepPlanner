from math import ceil
import streamlit as st

from Utils import LoadStyle
from Components import DashboardContainer , RecipesSelectors , GroceryListContainer

def Login():
    if 'SelectedRecipes' not in st.session_state:
        st.session_state['SelectedRecipes'] = {}
    
    MAX_CALORIES = 400
    st.session_state['MaxNutrientsValues'] = {
        'Calorías': MAX_CALORIES,
        'Carbohidratos': ceil(MAX_CALORIES*0.6/4),
        'Proteínas': ceil(MAX_CALORIES*0.15/4),
        'Grasas': ceil(MAX_CALORIES*0.25/9),
    }

def Main():
    LoadStyle()

    st.set_page_config(
        page_title = 'Meal Prep Planner',
        page_icon = '/app/static/Icon.png',
        layout = 'wide',
    )
    st.title(":color[Planificador de Menús Semanales]{foreground='#2391ff'}",text_alignment='center')

    Login()

    MenuCreation , GroceryList  = st.tabs(['**Creación del Menú**','**Lista de Compras**'])

    with MenuCreation:
        DashboardContainer()
        st.divider()
        RecipesSelectors()

    with GroceryList:
        GroceryListContainer()