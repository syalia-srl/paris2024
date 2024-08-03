import streamlit as st
import pandas as pd
from menu import menu
from app import download_data, download_domains


if not "data" in st.session_state:
    st.session_state["data"]=download_data()

if not "domains" in st.session_state:
    st.session_state["domains"]=download_domains()

domains = st.session_state["domains"]
data = st.session_state["data"]

sports = data["sports"]
events = data["events"]

sports_ids = [id for id in data["sports"]]
sports_names = [sports[id]["name"] for id in sports_ids]
sports_ids = ["Todos"] + sports_ids
sports_names = ["Todos"] + sports_names

st.header("Tabla de Medallas",divider=True)

sport_name = st.selectbox(
    "Seleccione el deporte:",
    sports_names,
    key="select_sport_table",
    help="Seleccione el deporte",
    label_visibility="visible",
)

finished_events = st.selectbox(
    "Seleccione los eventos:",
    ["Todos", "Eventos finalizados"],
    key="select_event_table",
    help="Seleccione los eventos",
    label_visibility="visible",
)

events_ended = False if finished_events == "Todos" else True

sport_id = (
    "Todos" if sport_name == "Todos" else sports_ids[sports_names.index(sport_name)]
)


def filter_predictions(sid, finished):
    ended = True
    predictions = []
    results = []
    for event in events.values():
        if (sid == "Todos") or (sid == event["sport"]):
            for s in event["sex"]:
                if (not finished) or (event["sex"][s]["finished"]):
                    predictions.append((event["sport"], event["sex"][s]["prediction"]))
                    results.append((event["sport"], event["sex"][s]["result"]))
                    if not event["sex"][s]["finished"]:
                        ended = False
    return ended, predictions, results


ended, predictions, results = filter_predictions(sport_id, events_ended)


def prediction_medals_count(predictions):
    countries = {}
    for id, p in predictions:
        for i in range(1, 4):
            domain = p[str(i)]["country_domain"]
            if not (domain in countries):
                countries[domain] = {1: 0, 2: 0, 3: 0}
            countries[domain][i] += 1
        if sports[id]["multiple_bronce"]:
            domain = p["4"]["country_domain"]
            if not (domain in countries):
                countries[domain] = {1: 0, 2: 0, 3: 0}
            countries[domain][3] += 1
    return countries


def result_medal_count(results):
    countries = {}
    for id, r in results:
        for i in range(1, 4):
            for item in r[str(i)]:
                domain = item["country_domain"]
                if not (domain in countries):
                    countries[domain] = {1: 0, 2: 0, 3: 0}
                countries[domain][i] += 1
        if sports[id]["multiple_bronce"]:
            for item in r["4"]:
                domain = item["country_domain"]
                if not (domain in countries):
                    countries[domain] = {1: 0, 2: 0, 3: 0}
                countries[domain][3] += 1
    return countries


if ended:
    if len(predictions) > 0:
        st.write("Todos los eventos seleccionados finalizaron")
    else:
        st.write("Aún no han concluido eventos ")
else:
    st.write("Todavía faltan por concluir algunos eventos")

if len(predictions) > 0:
    st.write("Tabla de Medallas:")

    col1, col2 = st.columns(2)

    with col1:
        p_medals = prediction_medals_count(predictions)

        p_countries = []
        p_names = []
        p_gold = []
        p_silver = []
        p_bronce = []
        p_total = []

        for country, medals in p_medals.items():
            p_countries.append(country)
            p_names.append(domains["to_names"][country.lower()])
            p_gold.append(medals[1])
            p_silver.append(medals[2])
            p_bronce.append(medals[3])
            p_total.append(medals[1] + medals[2] + medals[3])

        df_p = pd.DataFrame(
            {
                "CO": p_countries,
                "País": p_names,
                "Oro": p_gold,
                "Plata": p_silver,
                "Bronce": p_bronce,
                "Total": p_total,
            }
        )

        df_p = df_p.sort_values(by=["Oro", "Plata", "Bronce","País"], ascending=False)

        df_p.insert(0, "Po.", [i for i in range(1, len(df_p) + 1)], True)
        
        with st.container(border=True):
            st.write("Predicción:")

            st.dataframe(data=df_p, hide_index=True, height=round((len(df_p) + 1) * 35.3))

    if ended:
        with col2:
            r_medals = result_medal_count(results)

            r_countries = []
            r_names = []
            r_gold = []
            r_silver = []
            r_bronce = []
            r_total = []

            for country, medals in r_medals.items():
                r_countries.append(country)
                r_names.append(domains["to_names"][country.lower()])
                r_gold.append(medals[1])
                r_silver.append(medals[2])
                r_bronce.append(medals[3])
                r_total.append(medals[1] + medals[2] + medals[3])

            df_r = pd.DataFrame(
                {
                    "CO": r_countries,
                    "País": r_names,
                    "Oro": r_gold,
                    "Plata": r_silver,
                    "Bronce": r_bronce,
                    "Total": r_total,
                }
            )

            df_r = df_r.sort_values(by=["Oro", "Plata", "Bronce","País"], ascending=False)

            df_r.insert(0, "Po.", [i for i in range(1, len(df_r) + 1)], True)

            with st.container(border=True):

                st.write("Resultado:")

                st.dataframe(data=df_r, hide_index=True, height=round((len(df_r) + 1) * 35.3))

menu()
