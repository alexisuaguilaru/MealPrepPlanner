import streamlit as st

from Utils import GetIngredientsInformation

def GroceryListContainer():
    PrevRecipesID = [recipe['id'] for recipe in st.session_state['SelectedRecipes'].values()]
    ListIngredients = GetIngredientsInformation(PrevRecipesID)

    Ingredients , Selectors = st.columns([3,1])

    with Selectors:
        with st.container(vertical_alignment='center',horizontal_alignment='center'):
            st.markdown('##### **Número de Porciones**')
            NumServings = st.selectbox(
                '',
                list(range(1,1000)),
                label_visibility = 'collapsed',
            )
            
            TotalPricePerServing = (ListIngredients['TotalPrice']/ListIngredients['Servings']).sum()
            Total = TotalPricePerServing*NumServings
            st.markdown(
                f'##### **Costo por Total de Porciones:**',
                text_alignment = 'center',
            )
            st.markdown(
                f'##### **${Total:.2f} MXN**',
                text_alignment = 'center'
            )

    with Ingredients:
        Name , Amount , TotalCost = st.columns(3,border=True)

        with Name:
            st.markdown(
                "##### :color[Ingrediente]{foreground='#2391ff'}",
                text_alignment = 'center',
            )
        with Amount:
            st.markdown(
                "##### :color[Cantidad]{foreground='#2391ff'}",
                text_alignment = 'center',
            )
        with TotalCost:
            st.markdown(
                "##### :color[Costo total]{foreground='#2391ff'}",
                text_alignment = 'center',
            )

        for ingredient in ListIngredients.iloc:
            with Name:
                st.markdown(ingredient['Name'].capitalize())
            with Amount:
                amount = ingredient['Amount']*NumServings or ''
                unit = ingredient['Unit'] or ''
                amount_unit = ' '.join([str(amount),unit])
                if amount_unit != ' ':
                    st.markdown(amount_unit)
                else:
                    st.markdown(":color[0]{foreground='#ffffff'}")
            with TotalCost:
                st.markdown(f"${ingredient['TotalPrice']*NumServings:.2f} MXN")