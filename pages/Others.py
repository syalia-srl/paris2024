import streamlit as st
import pandas as pd
from menu import menu
from app import download_data
from datetime import date, timedelta

W = {
    "c1": 1,
    "c2": 1,
    "c3": 1,
    "c4": 1,
    "m1": 1,
    "m2": 1,
    "m3": 1,
    "m4": 1,
    "f1": 1,
    "f2": 1,
}

if not "data" in st.session_state:
    st.session_state["data"] = download_data()


data = st.session_state["data"]

sports = data["sports"]
events = data["events"]


def get_date_by_text(text):
    t = text.split("/")
    return date(int(t[0]), int(t[1]), int(t[2]))


def get_all_predictions():
    predictions = []
    for eid, e in events.items():
        for s in e["sex"]:
            temp = {
                "sport": e["sport"],
                "event": eid,
                "sex": s,
                "date": get_date_by_text(e["sex"][s]["date"]),
                "prediction": e["sex"][s]["prediction"],
                "ended": e["sex"][s]["finished"],
                "si": None,
                "lequipe": None,
            }
            if "others" in e["sex"][s]:
                if e["sex"][s]["others"][0]["name"] == "Sports Illustrated":
                    temp["si"] = e["sex"][s]["others"][0]["prediction"]
                    if len(e["sex"][s]) > 1:
                        temp["lequipe"] = e["sex"][s]["others"][1]["prediction"]
                else:
                    temp["lequipe"] = e["sex"][s]["others"][0]["prediction"]
                    if len(e["sex"][s]) > 1:
                        temp["si"] = e["sex"][s]["others"][1]["prediction"]
            predictions.append(temp)
    return predictions


def filter_by_ended(predictions):
    dpredictions = []
    for item in predictions:
        if item["ended"]:
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


def count_stats(predictions, keyword):
    champs = 0
    champs_in = 0
    champs_out = 0
    champs_fin = 0
    medalists = 0
    medalists_in = 0
    medalists_out = 0
    medalists_fin = 0
    inc = 0
    exact = 0
    finalists = 0
    for item in predictions:
        p = item[keyword]
        if sports[item["sport"]]["multiple_bronce"]:
            inc += 1
        if p["1"]["status"] != 0:
            finalists += 1
            champs_fin += 1
            medalists_fin += 1
            if p["1"]["status"] == 2:
                champs += 1
                champs_in += 1
                champs_out += 1
                medalists += 1
                exact += 1
                medalists_out += 1
                medalists_in += 1
            elif p["1"]["status"] == 3:
                medalists_out += 1
                medalists_in += 1
        if p["2"]["status"] != 0:
            finalists += 1
            medalists_fin += 1
            if p["2"]["status"] == 2:
                medalists += 1
                exact += 1
                medalists_out += 1
                medalists_in += 1
            elif p["2"]["status"] == 3:
                medalists_out += 1
                medalists_in += 1
            elif p["2"]["status"] == 4:
                champs_in += 1
                champs_out += 1
                medalists_out += 1
                medalists_in += 1
        if p["3"]["status"] != 0:
            finalists += 1
            medalists_fin += 1
            if p["3"]["status"] == 2:
                medalists += 1
                exact += 1
                medalists_out += 1
                medalists_in += 1
            elif p["3"]["status"] == 3:
                medalists_out += 1
                medalists_in += 1
            elif p["3"]["status"] == 4:
                champs_in += 1
                champs_out += 1
                medalists_out += 1
                medalists_in += 1
        if "4" in p and p["4"]["status"] != 0:
            finalists += 1
            if sports[item["sport"]]["multiple_bronce"]:
                medalists_fin += 1
            if p["4"]["status"] == 2:
                if sports[item["sport"]]["multiple_bronce"]:
                    medalists += 1
                    medalists_out += 1
                    medalists_in += 1
                exact += 1
            elif p["4"]["status"] == 3:
                medalists_out += 1
                if sports[item["sport"]]["multiple_bronce"]:
                    medalists_in += 1
            elif p["4"]["status"] == 4:
                champs_out += 1
                medalists_out += 1
                if sports[item["sport"]]["multiple_bronce"]:
                    champs_in += 1
                    medalists_in += 1
    return {
        "champs": champs,
        "champs_in": champs_in,
        "champs_out": champs_out,
        "champs_fin": champs_fin,
        "medalists": medalists,
        "medalists_in": medalists_in,
        "medalists_out": medalists_out,
        "medalists_fin": medalists_fin,
        "inc": inc,
        "exact": exact,
        "finalists": finalists,
    }


def percents_info(predictions, keyword):
    stats = count_stats(predictions, keyword)
    total = len(predictions)
    champs = round(stats["champs"] * 100 / total, 2)
    champs_in = round(stats["champs_in"] * 100 / total, 2)
    champs_out = round(stats["champs_out"] * 100 / total, 2)
    champs_fin = round(stats["champs_fin"] * 100 / total, 2)
    medalists = round(stats["medalists"] * 100 / (total * 3 + stats["inc"]), 2)
    medalists_in = round(stats["medalists_in"] * 100 / (total * 3 + stats["inc"]), 2)
    medalists_out = round(stats["medalists_out"] * 100 / (total * 3 + stats["inc"]), 2)
    medalists_fin = round(stats["medalists_fin"] * 100 / (total * 3 + stats["inc"]), 2)
    exact = round(stats["exact"] * 100 / (total * 8), 2)
    finalists = round(stats["finalists"] * 100 / (total * 8), 2)
    return {
        "total": total,
        "champs": champs,
        "champs_in": champs_in,
        "champs_out": champs_out,
        "champs_fin": champs_fin,
        "medalists": medalists,
        "medalists_in": medalists_in,
        "medalists_out": medalists_out,
        "medalists_fin": medalists_fin,
        "exact": exact,
        "finalists": finalists,
    }


st.header("Ranking de Pronósticos", divider=True)


all = get_all_predictions()
ended = filter_by_ended(all)

# for item in ended:
#     if item["si"]==None or item["lequipe"]==None:
#         st.write(item)

sports_group = group_predictions_by_sport(ended)

if len(ended) != 0:
    sports_names = ["Todos"]
    for s in sports_group:
        sports_names.append(s)
    sport_name = st.selectbox(
        "Seleccione el deporte:",
        sports_names,
        index=0,
        key="select_sport_table",
        help="Seleccione el deporte",
        label_visibility="visible",
    )

    if sport_name:
        st.write(sport_name)
        preds = ended
        if sport_name != "Todos":
            preds = sports_group[sport_name]
        pmatcom = percents_info(preds, "prediction")
        psi = percents_info(preds, "si")
        plequipe = percents_info(preds, "lequipe")

        labels = ["MATCOM", "Sports Illustrated", "L'Equipe"]
        total = [pmatcom["total"], psi["total"], plequipe["total"]]
        c1 = [pmatcom["champs"], psi["champs"], plequipe["champs"]]
        c2 = [pmatcom["champs_in"], psi["champs_in"], plequipe["champs_in"]]
        c4 = [pmatcom["champs_fin"], psi["champs_fin"], plequipe["champs_fin"]]
        m1 = [pmatcom["medalists"], psi["medalists"], plequipe["medalists"]]
        m2 = [pmatcom["medalists_in"], psi["medalists_in"], plequipe["medalists_in"]]
        m4 = [pmatcom["medalists_fin"], psi["medalists_fin"], plequipe["medalists_fin"]]
        g = [
            pmatcom["champs"] * W["c1"]
            + pmatcom["champs_in"] * W["c2"]
            + pmatcom["champs_fin"] * W["c4"]
            + pmatcom["medalists"] * W["m1"]
            + pmatcom["medalists_in"] * W["m2"]
            + pmatcom["medalists_fin"] * W["m4"],
            psi["champs"] * W["c1"]
            + psi["champs_in"] * W["c2"]
            + psi["champs_fin"] * W["c4"]
            + psi["medalists"] * W["m1"]
            + psi["medalists_in"] * W["m2"]
            + psi["medalists_fin"] * W["m4"],
            plequipe["champs"] * W["c1"]
            + plequipe["champs_in"] * W["c2"]
            + plequipe["champs_fin"] * W["c4"]
            + plequipe["medalists"] * W["m1"]
            + plequipe["medalists_in"] * W["m2"]
            + plequipe["medalists_fin"] * W["m4"],
        ]

        rk_p = pd.DataFrame(
            {
                "Pronósticos": labels,
                "Eventos": total,
                "C1": c1,
                "C2": c2,
                "C4": c4,
                "M1": m1,
                "M2": m2,
                "M4": m4,
                "G": g,
            }
        )

        rk_p = rk_p.sort_values(
            by=["G", "C1", "M1", "C2", "M2","C4","M4", "Eventos"], ascending=False
        )
        with st.expander("Métricas de evaluación", expanded=False):
            st.write("**C1**: porciento de campeones en su posición exacta")
            st.write("**C2**: porciento de campeones entre los medallistas")
            st.write("**C4**: porciento de campeones pronosticados entre los finalistas")
            st.write("**M1**: porciento de medallistas en su posición exacta")
            st.write("**M2**: porciento de medallistas entre los medallistas pronosticados")
            st.write("**M4**: porciento de medallistas pronosticados entre los finalistas")
            st.write("**G**: C1+C2+C4+M1+M2+M4")

        with st.expander("Ranking", expanded=True):
            st.dataframe(
                data=rk_p,
                hide_index=True,
                column_order=[
                    "Pronósticos",
                    "Eventos",
                    "C1",
                    "C2",
                    "C4",
                    "M1",
                    "M2",
                    "M4",
                    "G",
                ],
                height=round((len(rk_p) + 1) * 35.3),
            )


else:
    st.write("No ha concluido ningún evento")


menu()
