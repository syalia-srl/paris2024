import streamlit as st
import pandas as pd
from menu import menu
from app import download_data
from datetime import date, timedelta

W = {
    "c1":1,
    "c2":1,
    "m1":1,
    "m2":1,
    "f1":1,
    "f2":1
}

if not "data" in st.session_state:
    st.session_state["data"] = download_data()


data = st.session_state["data"]

sports = data["sports"]
events = data["events"]
authors = data["team"]


def get_date_by_text(text):
    t = text.split("/")
    return date(int(t[0]), int(t[1]), int(t[2]))


def get_all_predictions():
    predictions = []
    for eid, e in events.items():
        for s in e["sex"]:
            predictions.append(
                {
                    "sport": e["sport"],
                    "event": eid,
                    "sex": s,
                    "date": get_date_by_text(e["sex"][s]["date"]),
                    "prediction": e["sex"][s]["prediction"],
                    "ended": e["sex"][s]["finished"],
                }
            )
    return predictions


def filter_by_ended(predictions):
    dpredictions = []
    for item in predictions:
        if item["ended"]:
            dpredictions.append(item)
    return dpredictions


def filter_by_dates(start, end, predictions):
    dpredictions = []
    for item in predictions:
        date = item["date"]
        if start <= date <= end:
            dpredictions.append(item)
    return dpredictions


def group_predictions_by_sport(predictions):
    spredictions = {}
    for item in predictions:
        sname = sports[item["sport"]]["name"]
        if not sname in spredictions:
            spredictions[sname] = []
        spredictions[sname].append(item)
    return spredictions


def group_predictions_by_author(predictions):
    apredictions = {}
    for item in predictions:
        aname = authors[sports[item["sport"]]["prediction_by"]]["name"]
        if not aname in apredictions:
            apredictions[aname] = []
        apredictions[aname].append(item)
    return apredictions


def filter_group_by_quantities(min, max, group):
    ngroup = {}
    for k, v in group.items():
        if min <= len(v) <= max:
            ngroup[k] = v
    return ngroup


def count_stats(predictions):
    champs = 0
    champs_out = 0
    medalists = 0
    medalists_out = 0
    inc = 0
    exact = 0
    finalists = 0
    for item in predictions:
        p = item["prediction"]
        if p["1"]["status"] != 0:
            finalists += 1
            if p["1"]["status"] == 2:
                champs += 1
                champs_out += 1
                medalists += 1
                exact += 1
                medalists_out += 1
            elif p["1"]["status"] == 3:
                medalists_out += 1
        if p["2"]["status"] != 0:
            finalists += 1
            if p["2"]["status"] == 2:
                medalists += 1
                exact += 1
                medalists_out += 1
            elif p["2"]["status"] == 3:
                medalists_out += 1
            elif p["2"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
        if p["3"]["status"] != 0:
            finalists += 1
            if p["3"]["status"] == 2:
                medalists += 1
                exact += 1
                medalists_out += 1
            elif p["3"]["status"] == 3:
                medalists_out += 1
            elif p["3"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
        if p["4"]["status"] != 0:
            finalists += 1
            if p["4"]["status"] == 2:
                if sports[s]["multiple_bronce"]:
                    medalists += 1
                    inc += 1
                    medalists_out += 1
                exact += 1
            elif p["4"]["status"] == 3:
                medalists_out += 1
            elif p["4"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
        if p["5"]["status"] != 0:
            finalists += 1
            if p["5"]["status"] == 2:
                exact += 1
            elif p["5"]["status"] == 3:
                medalists_out += 1
            elif p["5"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
        if p["6"]["status"] != 0:
            finalists += 1
            if p["6"]["status"] == 2:
                exact += 1
            elif p["6"]["status"] == 3:
                medalists_out += 1
            elif p["6"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
        if p["7"]["status"] != 0:
            finalists += 1
            if p["7"]["status"] == 2:
                exact += 1
            elif p["7"]["status"] == 3:
                medalists_out += 1
            elif p["7"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
        if p["8"]["status"] != 0:
            finalists += 1
            if p["8"]["status"] == 2:
                exact += 1
            elif p["8"]["status"] == 3:
                medalists_out += 1
            elif p["8"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
    return {
        "champs": champs,
        "champs_out": champs_out,
        "medalists": medalists,
        "medalists_out": medalists_out,
        "inc": inc,
        "exact": exact,
        "finalists": finalists,
    }


def percents_info(predictions):
    stats = count_stats(predictions)
    total = len(predictions)
    champs = round(stats["champs"] * 100 / total, 2)
    champs_out = round(stats["champs_out"] * 100 / total, 2)
    medalists = round(stats["medalists"] * 100 / (total * 3 + stats["inc"]), 2)
    medalists_out = round(stats["medalists_out"] * 100 / (total * 3 + stats["inc"]), 2)
    exact = round(stats["exact"] * 100 / (total * 8), 2)
    finalists = round(stats["finalists"] * 100 / (total * 8), 2)
    return {
        "total": total,
        "champs": champs,
        "champs_out": champs_out,
        "medalists": medalists,
        "medalists_out": medalists_out,
        "exact": exact,
        "finalists": finalists,
    }


st.header("Ranking de Modelos", divider=True)


dates = st.slider(
    "Selecciona el periodo:",
    min_value=date(2024, 7, 27),
    max_value=date(2024, 8, 11),
    value=(date(2024, 7, 27), date(2024, 8, 11)),
    step=timedelta(days=1),
)

start = dates[0]
end = dates[1]

criteria = st.selectbox(
    "Seleccione el criterio del ranking:",
    ["Por deporte", "Por autor"],
    key="select_ranking_criteria",
    help="Seleccione el criterio",
    index=1,
    placeholder="Seleccione una opción",
    label_visibility="visible",
)

quantities = st.slider(
    "Selecciona el rango del número de predicciones:",
    min_value=1,
    max_value=52,
    value=(1, 52),
    step=1,
    key="slider_quantities",
)

minp = quantities[0]
maxp = quantities[1]


all = get_all_predictions()
ended = filter_by_ended(all)
all_info = percents_info(ended)

if len(ended) != 0:
    preds = filter_by_dates(start, end, ended)
    if len(preds) != 0:
        if criteria:
            name = None
            group = None
            if criteria == "Por deporte":
                group = group_predictions_by_sport(ended)
                name = "Deportes"
            else:
                group = group_predictions_by_author(ended)
                name = "Autores"
            group = filter_group_by_quantities(minp, maxp, group)
            if len(group) != 0:

                with st.expander("Métricas de evaluación",expanded=False):
                    st.write("**C1**: porciento de campeones en su posición exacta")
                    st.write("**C2**: porciento de campeones entre los finalistas")
                    st.write("**M1**: porciento de medallistas en su posición exacta")
                    st.write("**M2**: porciento de medallistas entre los finalistas")
                    st.write("**F1**: porciento de finalistas en su posición exacta")
                    st.write("**F2**: porciento de finalistas")
                    st.write("**G**: C1+C2+M1+M2+F1+F2")

                labels = []
                total = []
                c1 = []
                c2 = []
                m1 = []
                m2 = []
                f1 = []
                f2 = []
                g = []

                labels.append("Todos")
                total.append(all_info["total"])
                c1.append(all_info["champs"])
                c2.append(all_info["champs_out"])
                m1.append(all_info["medalists"])
                m2.append(all_info["medalists_out"])
                f1.append(all_info["exact"])
                f2.append(all_info["finalists"])
                g.append(
                    all_info["champs"]*W["c1"]
                    + all_info["champs_out"]*W["c2"]
                    + all_info["medalists"]*W["m1"]
                    + all_info["medalists_out"]*W["m2"]
                    + all_info["exact"]*W["f1"]
                    + all_info["finalists"]*W["f2"]
                )

                for k, v in group.items():
                    labels.append(k)
                    info = percents_info(v)
                    total.append(info["total"])
                    c1.append(info["champs"])
                    c2.append(info["champs_out"])
                    m1.append(info["medalists"])
                    m2.append(info["medalists_out"])
                    f1.append(info["exact"])
                    f2.append(info["finalists"])
                    g.append(
                        info["champs"]
                        + info["champs_out"]
                        + info["medalists"]
                        + info["medalists_out"]
                        + info["exact"]
                        + info["finalists"]
                    )

                rk = pd.DataFrame(
                    {
                        name: labels,
                        "Eventos": total,
                        "C1": c1,
                        "C2": c2,
                        "F1": f1,
                        "F2": f2,
                        "M1": m1,
                        "M2": m2,
                        "G": g
                    }
                )

                rk = rk.sort_values(by=["G", "C1", "M1","F1","C2","M2","F2","Eventos"], ascending=False)

                with st.expander("Ranking",expanded=True):
                    st.dataframe(data=rk,hide_index=True,column_order=[name,"Eventos","C1","C2","M1","M2","F1","F2","G"])

            else:
                st.write("No hay eventos concluidos para esos criterios")
    else:
        st.write("No hay eventos concluidos para esos criterios")
else:
    st.write("No hay eventos concluidos para esos criterios")

menu()
