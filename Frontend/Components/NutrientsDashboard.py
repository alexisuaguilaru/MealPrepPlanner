import streamlit as st

from Utils import GetGeneralRecipesInformation , GetProgressNutrient

NutrientsLabels = [
    'Calorías',
    'Carbohidratos',
    'Proteínas',
    'Grasas',
]
def DashboardContainer():
    PrevRecipesID = [recipe['id'] for recipe in st.session_state['SelectedRecipes'].values()]
    GeneralInformation = GetGeneralRecipesInformation(PrevRecipesID)
    GeneralInformation = _ExtractInformationToDict(GeneralInformation)

    with st.container(horizontal=True):
        DashboardColumns = st.columns(5)
        for nutrient , column in zip(NutrientsLabels,DashboardColumns):
            with column:
                progress_nutrient , color = GetProgressNutrient(
                    GeneralInformation[nutrient],
                    nutrient,
                )
                st.markdown(
                    progress_nutrient,
                    text_alignment = 'center',
                    unsafe_allow_html = True,
                )
                unit = 'grs' if nutrient != 'Calorías' else 'cals'
                st.markdown(
                    f":color[**{nutrient}** ({unit})]{{foreground={color}}}",
                    text_alignment = 'center'
                )
                st.markdown(
                    f"Max: {st.session_state['MaxNutrientsValues'][nutrient]} {unit}",
                    text_alignment = 'center'
                )
    st.markdown(':gray[Valores sustentados en una dieta cuyas comidas aportan 400 calorías en promedio.]')

def _ExtractInformationToDict(GeneralInformation):
    return {
        'Calorías': GeneralInformation.Calories,
        'Carbohidratos': GeneralInformation.Carbohydrates,
        'Proteínas': GeneralInformation.Proteins,
        'Grasas': GeneralInformation.Fats,
    }