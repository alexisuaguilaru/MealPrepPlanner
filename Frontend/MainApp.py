from itertools import product
import streamlit as st

from Utils import LoadStyle
from Components import RecipesSelectors

def Login():
    if 'SelectedRecipes' not in st.session_state:
        st.session_state['SelectedRecipes'] = {}

def Main():
    LoadStyle()

    st.set_page_config(
        page_title = 'Meal Prep Planner',
        page_icon = '/app/static/Icon.png',
        layout = 'wide',
    )
    st.title('Planificador de Menús Semanales',text_alignment='center')

    Login()

    RecipesSelectors()