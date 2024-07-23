import streamlit as st
import pandas as pd
import plotly.express as px
from menu import menu
from app import download_data


if not "data" in st.session_state:
    st.session_state["data"]=download_data()

data = st.session_state["data"]

sports = data["sports"]
events = data["events"]

sports_ids = [id for id in data["sports"]]
sports_names = [sports[id]["name"] for id in sports_ids]
sports_ids = ["Todos"] + sports_ids
sports_names = ["Todos"] + sports_names

sport_name = st.selectbox(
    "Seleccione el deporte:",
    sports_names,
    key="select_sport_table",
    help="Seleccione el deporte",
    label_visibility="visible",
)

sport_id = "Todos" if sport_name == "Todos" else sports_ids[sports_names.index(sport_name)]

def filter_events(sid):
    f_events = []
    for event in events.values():
        if (sid=="Todos") or (sid==event["sport"]):
            f_events.append(event)
    return f_events

def get_predictions(events):
    predictions = []
    for e in events:
        for s in e["sex"]:
            p = e["sex"][s]["prediction"]
            f = e["sex"][s]["finished"]
            s = e["sport"]
            predictions.append((f,p,s))
    return predictions


f_events = filter_events(sport_id)
t_predictions = get_predictions(f_events)
f_predictions = [p for p in t_predictions if p[0]]
n_tpred = len(t_predictions)
n_fpred = len(f_predictions)

with st.expander(f"{n_tpred}  eventos en total",True):
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.write(f"{n_tpred} eventos pronosticados de {n_tpred}")
            df_tp = pd.DataFrame(
                {
                    "type": ["Eventos sin pronóstico", "Eventos pronosticados"],
                    "data": [0,n_tpred]
                }
            )
            fig_tp = px.pie(df_tp, values='data', names='type',height=350,color="type",color_discrete_map={
                "Eventos sin pronóstico": "royalblue",
                "Eventos pronosticados": "darkblue"
            })
            fig_tp.update_layout(legend=dict(
                yanchor="bottom",
                y=-0.26,
                xanchor="left",
                x=0.25
            ))
            st.plotly_chart(fig_tp,use_container_width=True)
    
    with col2:
        ended = "eventos finalizados" if n_fpred!=1 else  "evento finalizado"
        with st.container(border=True):
            st.write(f"{n_fpred} {ended} de {n_tpred} pronosticados")
            df_fp = pd.DataFrame(
                {
                    "type": ["Eventos sin finalizar", "Eventos finalizados"],
                    "data": [n_tpred-n_fpred,n_fpred]
                }
            )
            fig_fp = px.pie(df_fp, values='data', names='type',height=350,color="type", color_discrete_map={
                "Eventos sin finalizar": "royalblue",
                "Eventos finalizados": "darkblue"
            })
            fig_fp.update_layout(legend=dict(
                yanchor="bottom",
                y=-0.26,
                xanchor="left",
                x=0.25
            ))
            st.plotly_chart(fig_fp,use_container_width=True)

def count_stats(predictions):
    champs = 0
    champs_out = 0
    medalists = 0
    medalists_out = 0
    inc = 0
    exact = 0
    finalists = 0
    for f,p,s in predictions:
        if p["1"]["status"]!=0:
            finalists+=1
            if p["1"]["status"]==2:
                champs += 1
                medalists +=1
                exact+=1
            elif p["1"]["status"]==3:
                medalists_out+=1
        if p["2"]["status"]!=0:
            finalists+=1
            if p["2"]["status"]==2:
                medalists+=1
                exact+=1
            elif p["2"]["status"]==3:
                medalists_out+=1
            elif p["2"]["status"]==4:
                champs_out+=1
        if p["3"]["status"]!=0:
            finalists+=1
            if p["3"]["status"]==2:
                medalists+=1
                exact+=1
            elif p["3"]["status"]==3:
                medalists_out+=1
            elif p["3"]["status"]==4:
                champs_out+=1
        if p["4"]["status"]!=0:
            finalists+=1
            if p["4"]["status"]==2:
                if sports[s]["multiple_bronce"]:
                    medalists+=1
                    inc += 1
                exact+=1
            elif p["4"]["status"]==3:
                medalists_out+=1
            elif p["4"]["status"]==4:
                champs_out+=1
        if p["5"]["status"]!=0:
            finalists+=1
            if p["5"]["status"]==2:
                exact+=1
            elif p["5"]["status"]==3:
                medalists_out+=1
            elif p["5"]["status"]==4:
                champs_out+=1
        if p["6"]["status"]!=0:
            finalists+=1
            if p["6"]["status"]==2:
                exact+=1
            elif p["6"]["status"]==3:
                medalists_out+=1
            elif p["6"]["status"]==4:
                champs_out+=1
        if p["7"]["status"]!=0:
            finalists+=1
            if p["7"]["status"]==2:
                exact+=1
            elif p["7"]["status"]==3:
                medalists_out+=1
            elif p["7"]["status"]==4:
                champs_out+=1
        if p["8"]["status"]!=0:
            finalists+=1
            if p["8"]["status"]==2:
                exact+=1
            elif p["8"]["status"]==3:
                medalists_out+=1
            elif p["8"]["status"]==4:
                champs_out+=1
    return {"champs":champs, "champs_out":champs_out,"medalists":medalists,"medalists_out":medalists_out,"inc":inc,"exact":exact,"finalists":finalists}

if n_fpred>0:
    
    with st.expander(f"{n_fpred}  eventos concluidos",True):
        
        stats = count_stats(f_predictions)
        
        fcol1, fcol2 = st.columns(2)
        
        with fcol1:
            with st.container(border=True):
                st.write(f"{stats['champs']} campeones pronosticados de {n_fpred} posibles" )
                df_g = pd.DataFrame(
                    {
                        "type": ["Campeones no pronosticados", "Campeones pronosticados"],
                        "data": [(n_fpred-stats['champs']),stats['champs']]
                    }
                )
                fig_g = px.pie(df_g, values='data', names='type',height=350,color="type", color_discrete_map={
                    "Campeones no pronosticados": "royalblue",
                    "Campeones pronosticados": "darkblue"
                })
                fig_g.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.26,
                    xanchor="left",
                    x=0.25
                ))
                st.plotly_chart(fig_g,use_container_width=True)

            with st.container(border=True):
                st.write(f"{stats['medalists']} medallistas de {n_fpred*3+stats['inc']} posibles" )
                df_m = pd.DataFrame(
                    {
                        "type": ["Medallistas no pronosticados", "Medallistas pronosticados"],
                        "data": [(n_fpred*3+stats['inc']-stats['medalists']),stats['medalists']]
                    }
                )
                fig_m = px.pie(df_m, values='data', names='type',height=350,color="type", color_discrete_map={
                    "Medallistas no pronosticados": "royalblue",
                    "Medallistas pronosticados": "darkblue"
                })
                fig_m.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.26,
                    xanchor="left",
                    x=0.25
                ))
                st.plotly_chart(fig_m,use_container_width=True)

            with st.container(border=True):
                st.write(f"{stats['exact']} posiciones exactas de {n_fpred*8} posibles" )
                df_m = pd.DataFrame(
                    {
                        "type": ["Posiciones erradas", "Posiciones exactas"],
                        "data": [(n_fpred*8-stats['exact']),stats['exact']]
                    }
                )
                fig_m = px.pie(df_m, values='data', names='type',height=350,color="type", color_discrete_map={
                    "Posiciones erradas": "royalblue",
                    "Posiciones exactas": "darkblue"
                })
                fig_m.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.26,
                    xanchor="left",
                    x=0.25
                ))
                st.plotly_chart(fig_m,use_container_width=True)

        with fcol2:
            with st.container(border=True):
                st.write(f"{stats['champs']+stats['champs_out']} campeones entre finalistas de {n_fpred} posibles" )
                
                df_m = pd.DataFrame(
                    {
                        "type": ["Campeones fuera de los finalistas", "Campeones entre los finalistas"],
                        "data": [n_fpred - stats['champs']+stats['champs_out'],stats['champs']+stats['champs_out']]
                    }
                )
                fig_m = px.pie(df_m, values='data', names='type',height=350,color="type", color_discrete_map={
                    "Campeones fuera de los finalistas": "royalblue",
                    "Campeones entre los finalistas": "darkblue"
                })
                fig_m.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.26,
                    xanchor="left",
                    x=0.25
                ))
                st.plotly_chart(fig_m,use_container_width=True)
            
            with st.container(border=True):
                st.write(f"{stats['medalists']+stats['medalists_out']} medallistas entre finalistas de {n_fpred*3+stats['inc']} posibles" )
                df_m = pd.DataFrame(
                    {
                        "type": ["Medallistas fuera de los finalistas", "Medallistas entre los finalistas"],
                        "data": [(n_fpred*3+stats['inc']-stats['medalists']-stats['medalists_out']),stats['medalists']+stats['medalists_out']]
                    }
                )
                fig_m = px.pie(df_m, values='data', names='type',height=350,color="type", color_discrete_map={
                    "Medallistas fuera de los finalistas": "royalblue",
                    "Medallistas entre los finalistas": "darkblue"
                })
                fig_m.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.26,
                    xanchor="left",
                    x=0.25
                ))
                st.plotly_chart(fig_m,use_container_width=True)
            
            with st.container(border=True):
                st.write(f"{stats['finalists']} finalistas de {n_fpred*8} posibles" )
                df_m = pd.DataFrame(
                    {
                        "type": ["Finalistas errados", "Finalistas acertados"],
                        "data": [(n_fpred*8-stats['finalists']),stats['finalists']]
                    }
                )
                fig_m = px.pie(df_m, values='data', names='type',height=350,color="type", color_discrete_map={
                    "Finalistas errados": "royalblue",
                    "Finalistas acertados": "darkblue"
                })
                fig_m.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.26,
                    xanchor="left",
                    x=0.25
                ))
                st.plotly_chart(fig_m,use_container_width=True)

menu() 
