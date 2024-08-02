import streamlit as st
import pandas as pd
import json, requests
from menu import menu
from app import download_data, download_domains

if not "data" in st.session_state:
    st.session_state["data"] = download_data()

if not "domains" in st.session_state:
    st.session_state["domains"] = download_domains()

data = st.session_state["data"]
domains = st.session_state["domains"]

sports = data["sports"]
events = data["events"]


coi_names = list(domains["to_names"].items())
coi_names.sort(key=lambda x: x[1])

names = [i[1] for i in coi_names]
abrvs = [i[0] for i in coi_names]


st.header("Pronóstico por Países", divider=True)


def get_predictions(cid):
    predictions = []
    check = set()
    for eid, e in events.items():
        for s in e["sex"]:
            for v in e["sex"][s]["prediction"].values():
                if v["country_domain"].lower() == cid:
                    if not (eid, s) in check:
                        predictions.append(
                            {
                                "sport": e["sport"],
                                "event": eid,
                                "sex": s,
                                "prediction": e["sex"][s]["prediction"],
                            }
                        )
                        check.add((eid, s))
                        break
    return predictions


def get_results(cid):
    results = []
    check = set()
    for eid, e in events.items():
        for s in e["sex"]:
            for r in e["sex"][s]["result"].values():
                for v in r:
                    if v["country_domain"].lower() == cid:
                        if not (eid, s) in check:
                            results.append(
                                {
                                    "sport": e["sport"],
                                    "event": eid,
                                    "sex": s,
                                    "result": e["sex"][s]["result"],
                                }
                            )
                            check.add((eid, s))
                            break

    return results


def filter_by_medalists(cid, predictions):
    preds = []
    for item in predictions:
        pred = item["prediction"]
        for place in pred:
            if (
                (place in ["1", "2", "3"])
                or ((place == "4") and (sports[item["sport"]]["multiple_bronce"]))
            ) and (cid == pred[place]["country_domain"].lower()):
                preds.append(item)
                break
    return preds


def filter_result_by_medalists(cid, predictions):
    preds = []
    for item in predictions:
        pred = item["result"]
        for place in pred:
            b=False
            for r in pred[place]:
                if (
                    (place in ["1", "2", "3"])
                    or ((place == "4") and (sports[item["sport"]]["multiple_bronce"]))
                ) and (cid == r["country_domain"].lower()):
                    preds.append(item)
                    b=True
                    break
            if b:
                break
    return preds


def replace_sex(sex):
    if sex == "female":
        return "Femenino"
    elif sex == "male":
        return "Masculino"
    return "Mixto"


def process_predictions(cid, predictions):
    info = {i: {"total": 0, "sports": {}} for i in range(1, 9)}
    for item in predictions:
        pred = item["prediction"]
        for place in pred:
            if cid == pred[place]["country_domain"].lower():
                index = int(place)
                if sports[item["sport"]]["multiple_bronce"] and place == "4":
                    index = 3
                info[index]["total"] += 1
                sport = sports[item["sport"]]["name"]
                if not sport in info[index]["sports"]:
                    info[index]["sports"][sport] = []
                info[index]["sports"][sport].append(
                    {
                        "name": pred[place]["name"],
                        "event": events[item["event"]]["name"],
                        "sex": replace_sex(item["sex"]),
                    }
                )
    return info


def process_results(cid, predictions):
    info = {i: {"total": 0, "sports": {}} for i in range(1, 9)}
    for item in predictions:
        res = item["result"]
        for place in res:
            for r in res[place]:
                if cid == r["country_domain"].lower():
                    index = int(place)
                    if sports[item["sport"]]["multiple_bronce"] and place == "4":
                        index = 3
                    info[index]["total"] += 1
                    sport = sports[item["sport"]]["name"]
                    if not sport in info[index]["sports"]:
                        info[index]["sports"][sport] = []
                    info[index]["sports"][sport].append(
                        {
                            "name": r["name"],
                            "event": events[item["event"]]["name"],
                            "sex": replace_sex(item["sex"]),
                        }
                    )
    return info


def convert_place(i):
    if i == 1:
        return "Oro"
    elif i == 2:
        return "Plata"
    elif i == 3:
        return "Bronce"
    elif i == 4:
        return "4to lugar"
    elif i == 5:
        return "5to lugar"
    elif i == 6:
        return "6to lugar"
    elif i == 7:
        return "7mo lugar"
    return "8vo lugar"


def generate_markdown(index, info):
    if not index in info or info[index]["total"] == 0:
        return "No hay deportistas pronosticados en esta posición"
    md = """"""
    for sport, items in info[index]["sports"].items():
        sport = f"""
            **{sport}**

        """
        md += sport
        for e in items:
            athlete = f"""
                - {e["name"]}
                  {e["event"]} - {e["sex"]}
            """
            md += athlete
    return md


country_name = st.selectbox(
    "Seleccione el país:",
    names,
    key="select_country",
    help="Seleccione el país",
    index=None,
    placeholder="Seleccione una opción",
    label_visibility="visible",
)

if country_name:
    country_domain = abrvs[names.index(country_name)]

    prediction_type = st.selectbox(
        "Seleccione el tipo de resultado:",
        ["Medallistas", "Finalistas"],
        key="select_type_pred",
        help="Seleccione el tipo de resultado",
        index=None,
        placeholder="Seleccione una opción",
        label_visibility="visible",
    )

    if prediction_type:
        predictions = get_predictions(country_domain)
        results = get_results(country_domain)

        last = 9
        if prediction_type == "Medallistas":
            predictions = filter_by_medalists(country_domain, predictions)
            results = filter_result_by_medalists(country_domain, results)
            last = 4


        country_sports = [
            (i, sports[i]["name"]) for i in list(set([p["sport"] for p in predictions]))
        ]
        rcountry_sports = [
            (i, sports[i]["name"]) for i in list(set([p["sport"] for p in results]))
        ]

        country_sports = list(set(country_sports).union(set(rcountry_sports)))

        country_sports.sort(key=lambda x: x[1])
        sport_names = ["Todos"] + [i[1] for i in country_sports]
        sport_ids = ["Todos"] + [i[0] for i in country_sports]

        sport_name = st.selectbox(
            "Seleccione el deporte:",
            sport_names,
            key="select_sport_pred",
            help="Seleccione el deporte",
            label_visibility="visible",
        )

        info = process_predictions(country_domain, predictions)
        rinfo = process_results(country_domain, results)

        if sport_name != "Todos":
            info = {
                i: {
                    "total": len(v["sports"][sport_name]),
                    "sports": {sport_name: v["sports"][sport_name]},
                }
                for i, v in info.items()
                if sport_name in v["sports"]
            }
            rinfo = {
                i: {
                    "total": len(v["sports"][sport_name]),
                    "sports": {sport_name: v["sports"][sport_name]},
                }
                for i, v in rinfo.items()
                if sport_name in v["sports"]
            }

        with st.container(border=True):
            st.write("Predicción:")
            for i in range(1, last):
                with st.expander(
                    f"{convert_place(i)}: {info[i]['total'] if i in info else 0}"
                ):
                    st.markdown(generate_markdown(i, info))

        with st.container(border=True):
            st.write("Resultado:")
            for i in range(1, last):
                with st.expander(
                    f"{convert_place(i)}: {rinfo[i]['total'] if i in rinfo else 0}"
                ):
                    st.markdown(generate_markdown(i, rinfo))

menu()
