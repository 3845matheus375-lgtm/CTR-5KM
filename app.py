import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="CTR-5KM", layout="centered")

st.title("CTR-5KM | Controle Estratégico 5km")

arquivo = "dados.csv"

# Carregar dados existentes
if os.path.exists(arquivo):
    dados = pd.read_csv(arquivo)
else:
    dados = pd.DataFrame(columns=["Data","Tipo","Distancia","Tempo","Pace","Peso"])

st.subheader("Registrar Treino")

with st.form("form_treino"):
    data = st.date_input("Data")
    tipo = st.selectbox("Tipo de treino", ["Corrida", "Bike", "Força"])
    distancia = st.number_input("Distância (km)", min_value=0.0)
    tempo = st.number_input("Tempo (minutos)", min_value=0.0)
    peso = st.number_input("Peso atual (kg)", min_value=0.0)
    
    submit = st.form_submit_button("Salvar")

if submit:
    if distancia > 0:
        pace = tempo / distancia
    else:
        pace = 0
    
    novo = pd.DataFrame(
        [[data, tipo, distancia, tempo, round(pace, 2), peso]],
        columns=dados.columns
    )
    
    dados = pd.concat([dados, novo], ignore_index=True)
    dados.to_csv(arquivo, index=False)
