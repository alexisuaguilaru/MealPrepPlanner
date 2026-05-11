import streamlit as st

from Utils import GetIngredientsInformation

def GroceryListContainer():
    PrevRecipesID = [recipe['id'] for recipe in st.session_state['SelectedRecipes'].values()]
    ListIngredients = GetIngredientsInformation(PrevRecipesID)

    Ingredients , Selectors = st.columns([3,1])

    with Ingredients:
        Name , Amount , TotalPrice = st.columns(3,border=True)

        with Name:
            st.markdown(
                "###### :color[Ingrediente]{foreground='#2391ff'}",
                text_alignment = 'center',
            )
        with Amount:
            st.markdown(
                "###### :color[Cantidad]{foreground='#2391ff'}",
                text_alignment = 'center',
            )
        with TotalPrice:
            st.markdown(
                "###### :color[Precio total]{foreground='#2391ff'}",
                text_alignment = 'center',
            )

        for ingredient in ListIngredients.iloc:
            with Name:
                st.markdown(ingredient['Name'].capitalize())
            with Amount:
                amount = ingredient['Amount'] or ''
                unit = ingredient['Unit'] or ''
                amount_unit = ' '.join([str(amount),unit])
                st.markdown(amount_unit)
            with TotalPrice:
                st.markdown(f"${ingredient['TotalPrice']:.2f} MXN")

    with Selectors:
        with st.container(vertical_alignment='center',horizontal_alignment='center'):
            NumServings = st.selectbox(
                '**Número de Porciones**',
                list(range(1,1000)),
            )
            
            TotalPricePerServing = (ListIngredients['TotalPrice']/ListIngredients['Servings']).sum()
            Total = TotalPricePerServing*NumServings

            st.markdown(
                f"""
                **Costo por total de porciones:**

                **${Total:.2f} MXN**
                """,
                text_alignment = 'center'
            )