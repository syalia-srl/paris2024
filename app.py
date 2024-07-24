import streamlit as st 
from menu import menu
import json, requests

st.set_page_config(
    page_title="Pronosticando Paris 2024 "
)

st.header('Pronosticando Paris 2024')


def download_data():
    url = st.secrets.jsons.data
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data

def download_domains():
    url = st.secrets.jsons.domains
    resp = requests.get(url)
    domains = json.loads(resp.text)
    return domains

SEXS = {
    "Masculino": "male",
    "Femenino": "female",
    "Mixto": "mixed"
}

if not "data" in st.session_state:
    st.session_state["data"]=download_data()


markdown = """
Los Juegos de la XXXIII Olimpiada, [París 2024](https://olympics.com/es/paris-2024), se efectuarán del 26 de julio al 11 de agosto en la capital de Francia. 
En ese período miles de atletas del mundo entero se enfentrarán por obtener las medallas en todos los deportes convocados.

Este proyecto propone las pronósticos de cada uno de los 329 eventos convocados. Por cada evento, se realizó
un modelo computacional que, basado en datos de los equipos y atletas clasificados, predice los posibles medallistas así como
a los atletas que quedarían entre los 8 primeros de cada especialidad. Asimismo, teniendo todos los resultados, también se pudo
predecir la tabla de medallas final de los juegos.

Esta puede ser una herramienta para disfrutar de mejor manera la Olimpiada teniendo a mano una guía para seguir a los deportistas
que podrían tener grandes resultados o conocer las posibles sorpresas, que seguro habrá bastantes.

En [Predicciones](/Predictions) pueden consultar los pronóstico de cada evento y, si el evento finalizó, compararlo con el resultado final en la 
competencia. En [Estadísticas](/Predictions_Stats) se pueden consultar, en general y por cada deporte convocado, el comportamiento de los pronósticos bajo 
distintas métricas. En [Tabla de Medallas](/Medal_Table) se pueden ver, en general y por cada deporte, las medallas pronósticadas y compararlas con las 
que se logren en la medida que concluyan los eventos. Finalmente, en [Países](/Countries) se pueden consultar los pronósticos de medallas y finalistas para cada 
país detallando los deportistas, eventos y deportes.

El proyecto fue desarrollado en su totalidad poe estudiantes y profesores del [Grupo de Inteligencia Artificial y Ciencia de Datos](https://gia-uh.github.io/) de la [Facultad de Matemática 
y Computación](https://matcom.uh.cu) de la [Universidad de La Habana](https://www.uh.cu) en colaboración con la empresa [Syalia S.R.L.](https://www.syalia.com) y el 
proyecto [Postdata.club](https://postdataclub.github.io). 
"""

st.markdown(markdown)

menu()
