import streamlit as st
import pandas as pd
from funcoes.fx_exibicao_df import exibir_df_aggrid
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

st.title(" Invest View")
st.write(" #### Consolidação do Extrato de Movimentações da B3")

# # Usuário carregará 1 ou mais relaórios de movimentação.
arquivos = st.file_uploader("📂 Carregue 1 arquivo para cada ano:", type=["xlsx", "xls"], accept_multiple_files=True)


if arquivos: # If para não aparecer um df vazio de início.

    df_movimentacoes = unificar_extratos_em_df(arquivos)
    with st.expander("Dados carregados"): # Exp1
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
    # st.dataframe(df_movimentacoes)


    with st.expander("Extrato de Movimentações B3 Organizado"): # Exp2
        exibir_df_aggrid(df_movimentacoes, altura=275)#, tema="balham-dark")

# ================================================================================================
    with st.expander("Teste"):  # ExpTeste
        import yfinance as yf  # cotação

        lista_ativos = ['BBAS3.SA', 'TAEE11.SA', 'BRBI11.SA', 'CSMG3.SA', 'PETR4.SA', 'VALE3.SA', 'BBSE3.SA',
                        'ISAE4.SA', 'HASH11.SA', 'IVVB11.SA', 'MXRF11.SA', 'HGLG11.SA']
        data_api = '2025-04-17'
        df_cotacao = yf.download(lista_ativos, start=data_api, progress=False, auto_adjust=False)['Close']  # Suprime a barra de progresso
        df_cotacao





