import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="CTR-5KM", layout="centered")

st.title("CTR-5KM | Painel Estratégico 5km")

arquivo = "dados.csv"

# Função para formatar pace
def formatar_pace(pace):
    minutos = int(pace)
    segundos = int((pace - minutos) * 60)
    return f"{minutos}:{segundos:02d}/km"

# Carregar dados
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
        [[data, tipo, distancia, tempo, pace, peso]],
        columns=dados.columns
    )
    
    dados = pd.concat([dados, novo], ignore_index=True)
    dados.to_csv(arquivo, index=False)
    
    st.success("Treino registrado!")

# Mostrar histórico
st.subheader("Histórico")
if not dados.empty:
    dados["Pace_formatado"] = dados["Pace"].apply(lambda x: formatar_pace(x) if x > 0 else "-")
    st.dataframe(dados[["Data","Tipo","Distancia","Tempo","Pace_formatado","Peso"]])

    # Volume semanal
    volume_total = dados["Distancia"].sum()
    st.metric("Volume Total (km)", round(volume_total,1))

    # Melhor tempo 5km
    corridas_5k = dados[(dados["Tipo"]=="Corrida") & (dados["Distancia"]>=5)]
    if not corridas_5k.empty:
        melhor_tempo = corridas_5k["Tempo"].min()
        progresso = max(0, min(100, (30 - melhor_tempo) / 5 * 100))
        st.metric("Melhor Tempo 5km", f"{melhor_tempo:.2f} min")
        st.progress(progresso)

    # Gráfico peso
    st.subheader("Evolução do Peso")
    st.line_chart(dados["Peso"])
