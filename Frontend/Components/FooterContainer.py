import streamlit as st

def Footer():
    st.divider()

    with st.container(horizontal=True,vertical_alignment='center',horizontal_alignment='center'):
        st.markdown(
            '[![](/app/static/School.png)](https://www.enesmorelia.unam.mx)',
            width = 100,
            text_alignment = 'left',
        )

        st.space('medium')

        st.markdown(
            '[**Alexis Aguilar**](https://github.com/alexisuaguilaru)',
            text_alignment = 'center',
        )

        st.space('medium')

        st.markdown(
            '[![](/app/static/Bachelors.png)](https://www.enesmorelia.unam.mx/licenciaturas/tecnologias-para-la-informacion-en-ciencias/)',
            width = 50,
            text_alignment = 'right',
        )