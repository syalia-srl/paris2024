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
print(coi_names)
names = [i[1] for i in coi_names]
abrvs = [i[0] for i in coi_names]




def get_predictions(cid):
    predictions = []
    for eid, e in events.items():
        for s in e["sex"]:
            for v in e["sex"][s]["prediction"].values():
                if v["country_domain"].lower() == cid:
                    predictions.append(
                        {
                            "sport": e["sport"],
                            "event": eid,
                            "sex": s,
                            "prediction": e["sex"][s]["prediction"],
                        }
                    )
                    break
    return predictions


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
    return preds

def replace_sex(sex):
    if sex=="female":
        return "Femenino"
    elif sex=="male":
        return "Masculino"
    return "Mixto"

def process_predictions(cid,predictions):
    info = { i: {"total": 0,"sports": {}} for i in range(1,9)}
    for item in predictions:
        pred = item["prediction"]
        for place in pred:
            if cid == pred[place]["country_domain"].lower():
                index = int(place)
                if sports[item["sport"]]["multiple_bronce"] and place=="4":
                    index = 3
                info[index]["total"]+=1
                sport = sports[item["sport"]]["name"] 
                if not sport in info[index]["sports"]:
                    info[index]["sports"][sport] = []
                info[index]["sports"][sport].append(
                    {
                        "name": pred[place]["name"],
                        "event": events[item["event"]]["name"],
                        "sex": replace_sex(item["sex"])
                    }
                )
    return info
    

def convert_place(i):
    if i==1:
        return "Oro"
    elif i==2:
        return "Plata"
    elif i==3:
        return "Bronce"
    elif i==4:
        return "4to lugar"
    elif i==5:
        return "5to lugar"
    elif i==6:
        return "6to lugar"
    elif i==7:
        return "7mo lugar"
    return "8vo lugar"

def generate_markdown(index,info):
    if not index in info or info[index]["total"]==0:
        return "No hay deportistas pronosticados en esta posición"
    md = """"""
    for sport,items in info[index]["sports"].items():
        sport = f"""
            **{sport}**

        """
        md+=sport
        for e in items:
            athlete = f"""
                - {e["name"]}
                  {e["event"]} - {e["sex"]}
            """
            md+=athlete
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

        last = 9
        if prediction_type=="Medallistas":
            predictions = filter_by_medalists(country_domain,predictions)
            last = 4
        

        country_sports = [
            (i, sports[i]["name"]) for i in list(set([p["sport"] for p in predictions]))
        ]
        
        country_sports.sort(key=lambda x: x[1])
        sport_names = ["Todos"]+[i[1] for i in country_sports]
        sport_ids = ["Todos"]+[i[0] for i in country_sports]

        sport_name = st.selectbox(
            "Seleccione el deporte:",
            sport_names,
            key="select_sport_pred",
            help="Seleccione el deporte",
            label_visibility="visible"
        )

        info =  process_predictions(country_domain,predictions)

        if sport_name!="Todos":
            info ={i:{"total":len(v["sports"][sport_name]),"sports": {sport_name: v["sports"][sport_name]}} for i,v in info.items() if sport_name in v["sports"]}
        

        for i in range(1,last):
            with st.expander(f"{convert_place(i)}: {info[i]['total'] if i in info else 0}"):
                st.markdown(generate_markdown(i,info))

menu()
