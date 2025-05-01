import streamlit as st
from funcoes.movimentacoes.fx_trat_movimentacoes import (
    unificar_extratos_em_df,
    tratar_coluna_data,
    tratar_colunas_numericas,
    negativar_valores_debito,
    criar_coluna_tipo_ativo,
    criar_coluna_ativo,
    atualizar_ticker,
    aplicar_desdobro,
)
from funcoes.movimentacoes.fx_exib_movimentacoes import (
    exibir_df_mov_filtrado,
    calcular_compras,
    calcular_vendas,
    calcular_remuneracoes,
)

st.title("📊 Invest View")
st.write(" #### 🔎 Consolidação do Extrato de Movimentações da B3")

# -----------------------------------------------------------------------------------------------------------------


with st.expander("📂 Carregamento dos dados", expanded=True): # Comentar e manter apenas para manutenção
    with st.container(border=True):
        # Usuário carregará 1 ou mais arquivos de extrato de movimentação
        arquivos = st.file_uploader("Carregue seus extratos de movimentação aqui, sendo 1 arquivo para cada ano:",
                                    type=["xlsx", "xls"], accept_multiple_files=True)


if arquivos: # If para não aparecer um df vazio de início

    # Cria o df_mov
    df_movimentacoes = unificar_extratos_em_df(arquivos)
    # with st.expander("Dados carregados"): # Comentar e manter apenas para manutenção
    #     st.dataframe(df_movimentacoes)


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

# -----------------------------------------------------------------------------------------------------------------
#     Expanded para Inicar aberto para carregar aggrid corretamente
    with st.expander("📃 Extrato de Movimentações B3", expanded=True):
        st.text("Info", help="Aplique filtros na tabela para que os indicadores abaixo se ajustem.")  # ℹ️
        # Nesse caso, ao chamar a fx, já é criado e exibido o df
        with st.container(border=True):
            # st.write('Aplique filtros na tabela para que os indicadores abaixo se ajustem')
            df_mov_filtrado = exibir_df_mov_filtrado(df_movimentacoes)#, tema="balham-dark")

        # Criando colunas dentro do expander ------ Indicadores:
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            with st.container(border=True):
                calcular_compras(df_mov_filtrado)

        with col2:
            with st.container(border=True):
                calcular_vendas(df_mov_filtrado)

        with col3:
            with st.container(border=True):
                calcular_remuneracoes(df_mov_filtrado)


# ================================================================================================
    with st.expander("Teste de cotação YF", expanded=True):  # ExpTeste
        import yfinance as yf  # cotação

        lista_ativos = ['BBAS3.SA', 'TAEE11.SA', 'BRBI11.SA', 'CSMG3.SA', 'PETR4.SA', 'VALE3.SA', 'BBSE3.SA',
                        'ISAE4.SA', 'HASH11.SA', 'IVVB11.SA', 'MXRF11.SA', 'HGLG11.SA']
        data_api = '2025-04-28'
        df_cotacao = yf.download(
            lista_ativos,
            start=data_api,
            auto_adjust=False, # Se for cruzar dados c/ div em separado, deixar auto_adjust=False é melhor, senão conta o div duas vezes.
            progress=False, # barra de progresso
        )['Close']  # Escolhe coluna
        df_cotacao

      # ------------------------------------------------------teste2
    st.write('teste 2')
    lista_ativos = ['BBAS3.SA',]
    df_cotacao2 = yf.download(
        lista_ativos,
        period = "1d",
        auto_adjust=False,
        progress=False,  # barra de progresso
        threads=False,
    )['Close']  # Escolhe coluna
    df_cotacao2
# antes:
# depois subir o codigo com data de 30/04 e testar cotação YF

      # ------------------------------------------------------


# -----------------------------
# Quando for criar o df_mov_financeiras, talvez seja melhor usar a mesma fx que cria o df_mov, mas já com o nome df_mov_fin,
# pois assim é um jeito de o df_mov_fin ser totalmente independente do df_mov. Se for mesmo fazer isso, depois por obs na fx:
# informando que ela é usada como ponto de partida dos dfs mov e mov_fin. Mas antes tentar pegar o df_mov pronto mesmo pois
# acho que dá


# qdo for ensinar usuario a usar talvez por link para cada explicação ou tentar ?info?


