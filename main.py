import streamlit as st
import pandas as pd

# Configurar o layout da página para ocupar toda a largura
st.set_page_config(layout="wide") # Fiz isso pra tabela não ficar pequena e com scroll horizontal.


st.title("📂 Upload de Múltiplos Arquivos Excel")


arquivos = st.file_uploader("Envie seus arquivos Excel", type=["xlsx", "xls"], accept_multiple_files=True)
if arquivos:
    for arquivo in arquivos:
        with st.expander(f"🔍 Visualizar: {arquivo.name}"):
            df = pd.read_excel(arquivo, sheet_name=0)  # Apenas a primeira aba
            st.dataframe(df, use_container_width=True)