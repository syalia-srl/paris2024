import streamlit as st
import pandas as pd
from menu import menu
from app import SEXS
from app import download_data


if not "data" in st.session_state:
    st.session_state["data"] = download_data()

data = st.session_state["data"]

sports = data["sports"]
events = data["events"]

sports_ids = [id for id in data["sports"]]
sports_names = [sports[id]["name"] for id in sports_ids]


def get_sport_sexs(sport_id):
    sexs = set()
    for event in events.values():
        if event["sport"] == sport_id:
            if "female" in event["sex"]:
                sexs.add("Femenino")
            if "male" in event["sex"]:
                sexs.add("Masculino")
            if "mixed" in event["sex"]:
                sexs.add("Mixto")
    sexs = list(sexs)
    sexs.sort()
    return sexs


def get_sport_events(sport_id, sex):
    events_names = []
    events_ids = []
    for id, event in events.items():
        if event["sport"] == sport_id:
            if sex in event["sex"]:
                events_ids.append(id)
                events_names.append(event["name"])
    return events_names, events_ids


sport_name = st.selectbox(
    "Seleccione el deporte:",
    sports_names,
    key="select_sport_prediction",
    help="Seleccione el deporte",
    index=None,
    placeholder="Seleccione una opción",
    label_visibility="visible",
)

if sport_name:
    sport_id = sports_ids[sports_names.index(sport_name)]
    sport_sexs = get_sport_sexs(sport_id)

    sport_sex = st.selectbox(
        "Seleccione el sexo:",
        sport_sexs,
        key="select_sport_prediction_sex",
        help="Seleccione el sexo",
        index=None,
        placeholder="Seleccione una opción",
    )

    if sport_sex:
        sport_sex = SEXS[sport_sex]
        sport_events_names, sport_events_ids = get_sport_events(sport_id, sport_sex)

        sport_event_name = st.selectbox(
            "Seleccione el evento:",
            sport_events_names,
            key="select_sport_prediction_event",
            help="Seleccione el evento",
            index=None,
            placeholder="Seleccione una opción",
        )

        if sport_event_name:
            sport_event_id = sport_events_ids[
                sport_events_names.index(sport_event_name)
            ]
            finished = events[sport_event_id]["sex"][sport_sex]["finished"]
            prediction = events[sport_event_id]["sex"][sport_sex]["prediction"]
            result = events[sport_event_id]["sex"][sport_sex]["result"]
            m_places = []
            m_names = []
            m_countries = []
            m_status = []
            mr_places = []
            mr_names = []
            mr_countries = []
            for i in range(1, 4):
                m_places.append(i)
                mr_places.append(i)
                m_names.append(prediction[str(i)]["name"])
                mr_names.append(result[str(i)][0]["name"])
                m_countries.append(prediction[str(i)]["country_domain"])
                mr_countries.append(result[str(i)][0]["country_domain"])
                m_status.append(prediction[str(i)]["status"])
            start_finalists = 4
            if sports[sport_id]["multiple_bronce"]:
                m_places.append(3)
                mr_places.append(3)
                m_names.append(prediction["4"]["name"])
                mr_names.append(result["4"][0]["name"])
                m_countries.append(prediction["4"]["country_domain"])
                mr_countries.append(result["4"][0]["country_domain"])
                m_status.append(prediction["4"]["status"])
                start_finalists = 5
            f_places = []
            f_names = []
            f_countries = []
            f_status = []
            fr_places = []
            fr_names = []
            fr_countries = []
            for i in range(start_finalists, 9):
                f_places.append(i)
                fr_places.append(i)
                f_names.append(prediction[str(i)]["name"])
                fr_names.append(result[str(i)][0]["name"])
                f_countries.append(prediction[str(i)]["country_domain"])
                fr_countries.append(result[str(i)][0]["country_domain"])
                f_status.append(prediction[str(i)]["status"])
            df_m = pd.DataFrame(
                {
                    "Lugar": m_places,
                    "Nombre": m_names,
                    "Pais": m_countries,
                    "status": m_status,
                }
            )
            df_mr = pd.DataFrame(
                {"Lugar": mr_places, "Nombre": mr_names, "Pais": mr_countries}
            )
            df_f = pd.DataFrame(
                {
                    "Lugar": f_places,
                    "Nombre": f_names,
                    "Pais": f_countries,
                    "status": f_status,
                }
            )
            df_fr = pd.DataFrame(
                {
                    "Lugar": fr_places,
                    "Nombre": fr_names,
                    "Pais": fr_countries,
                    "status": f_status,
                }
            )

            def color_coding(row):
                if row.status == 2:
                    return ["background-color:dodgerblue"] * len(row)
                elif row.status == 1:
                    return ["background-color:limegreen"] * len(row)
                elif row.status == 3:
                    return ["background-color:coral"] * len(row)
                elif row.status == 4:
                    return ["background-color:darkorchid"] * len(row)
                return ["text-decoration:line-through"] * len(row)

            if finished:
                st.write("El evento ya concluyó")
                legend = """
                Leyenda:

                ⯀ En su posición exacta ⯀ Fuera de su posición 
                
                ⯀ Medallista fuera de posición ⯀ Campeón fuera de posición
                """
                #st.markdown(legend)
            else:
                st.write("El evento aún no ha concluido")

            with st.expander("Medallistas", True):
                mcol1, mcol2 = st.columns(2)
                with mcol1:
                    with st.container(border=True):
                        st.write("Predicción:")
                        st.dataframe(
                            data=df_m.style.apply(color_coding, axis=1),
                            hide_index=True,
                            column_config={"status": None},
                        )
                if finished:
                    with mcol2:
                        with st.container(border=True):
                            st.write("Resultado:")
                            st.dataframe(data=df_mr, hide_index=True)

            with st.expander("Otros candidatos", True):
                fcol1, fcol2 = st.columns(2)
                with fcol1:
                    with st.container(border=True):
                        st.write("Prediccióon:")
                        st.dataframe(
                            data=df_f.style.apply(color_coding, axis=1),
                            hide_index=True,
                            column_config={"status": None},
                        )
                if finished:
                    with fcol2:
                        with st.container(border=True):
                            st.write("Resultados:")
                            st.dataframe(data=df_fr, hide_index=True)


menu()
