import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Triagem WhatsApp", layout="wide")

st.title("📊 Análise de Mensagens - Triagem Inteligente")
st.markdown("Dashboard para monitoramento de Fraudes, Assédios e Reclamações.")

# 1. Carregamento dos dados
try:
    with open("resultado_final_20.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    df = pd.DataFrame(dados)

    # 2. Métricas principais (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Mensagens", len(df))
    col2.metric("Possíveis Fraudes", len(df[df['classificacao'] == 'Fraude']))
    col3.metric("Casos de Assédio", len(df[df['classificacao'] == 'Assédio']))
    col4.metric("Reclamações", len(df[df['classificacao'] == 'Reclamação']))

    st.divider()

    # 3. Visualização Gráfica
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribuição por Classificação")
        fig_pizza = px.pie(df, names='classificacao', color='classificacao',
                           color_discrete_map={'Fraude':'red', 'Assédio':'orange', 'Reclamação':'blue', 'Outro':'gray'})
        st.plotly_chart(fig_pizza)

    with c2:
        st.subheader("Encaminhamento por Setor")
        fig_barra = px.bar(df['setor_encaminhado'].value_counts(), labels={'value':'Quantidade', 'index':'Setor'})
        st.plotly_chart(fig_barra)

    # 4. Tabela de dados detalhada
    st.subheader("🔍 Detalhamento das Mensagens")
    st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("Arquivo 'resultado_final_20.json' não encontrado. Processe as mensagens primeiro!")