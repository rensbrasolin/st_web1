import streamlit as st
import pandas as pd
from funcoes.movimentacoes.fx_movimentacoes import (
    unificar_extratos_em_df,
    tratar_coluna_data,
    tratar_colunas_numericas,
    negativar_valores_debito,
    criar_coluna_tipo_ativo,
    criar_coluna_ativo,
    atualizar_ticker,
    aplicar_desdobro,
)


st.title(" Consolidação do Extrato de Movimentações da B3")

# # Usuário carregará 1 ou mais relaórios de movimentação.
arquivos = st.file_uploader("📂 Carregue 1 arquivo para cada ano:", type=["xlsx", "xls"], accept_multiple_files=True)


if arquivos: # If para não aparecer um df vazio de início.

    df_movimentacoes = unificar_extratos_em_df(arquivos)
    with st.expander("Dados carregados"):
        st.dataframe(df_movimentacoes)


    df_movimentacoes = tratar_coluna_data(df_movimentacoes,'Data')
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = tratar_colunas_numericas(df_movimentacoes, ['Preço unitário', 'Quantidade', 'Valor da Operação'])
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = negativar_valores_debito(df_movimentacoes, ['Preço unitário', 'Quantidade', 'Valor da Operação'])
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = criar_coluna_ativo(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = criar_coluna_tipo_ativo(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = atualizar_ticker(df_movimentacoes)
    # st.dataframe(df_movimentacoes)

    df_movimentacoes = aplicar_desdobro(df_movimentacoes)
    with st.expander("Extrato de Movimentações B3 Organizado"):
        st.dataframe(df_movimentacoes)
