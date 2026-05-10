import streamlit as st

def LoadStyle():
    with open('./Frontend/Style.css',) as css_file:
        return st.markdown(
            f'<style>{css_file.read()}</style>',
            unsafe_allow_html = True
        )