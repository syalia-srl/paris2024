import streamlit as st

def menu():
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/Predictions.py",label="Predicciones")
    st.sidebar.page_link("pages/Predictions_Stats.py",label="Estadísticas")
    st.sidebar.page_link("pages/Medal_Table.py", label="Tabla de Medallas")
    st.sidebar.page_link("pages/Countries.py", label="Países")
    st.sidebar.page_link("pages/Ranking.py", label="Ranking de Modelos")
    st.sidebar.page_link("pages/Others.py", label="Ranking de Pronósticos")
    st.sidebar.page_link("pages/Team.py", label="Equipo")
