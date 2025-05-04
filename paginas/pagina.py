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

from funcoes.consolidacoes.fx_df_mov_financeiras import criar_df_mov_financeiras

from funcoes.consolidacoes.cotacao.fx_cotacao_yf import criar_df_cotacao_yf
from funcoes.consolidacoes.cotacao.fx_cotacao_trading_view_b3 import criar_df_cotacao_tvb3
# from funcoes.consolidacoes.cotacao.fx_cotacao_status_invest import obter_cotacoes_statusinvest
from funcoes.consolidacoes.cotacao.fx_cotacao_status_invest import criar_df_cotacao_statusinvest

st.title("📊 Invest View")
st.write(" #### 🔎 Consolidação do Extrato de Movimentações da B3")

# --------------------------------------------------------------------------------- CARREGANDO ARQ E CRIANDO DF MOV - 1


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

# ------------------------------------------------------------------------------------------------- EXIBINDO DF MOV - 2
#     Expanded para Inicar aberto para carregar aggrid corretamente
    with st.expander("📃 Extrato de Movimentações B3", expanded=True):
        st.text("Info", help="Aplique filtros na tabela para que os indicadores abaixo se ajustem.")  # ℹ️
        # Nesse caso, ao chamar a fx, já é criado e exibido o df aggrid
        with st.container(border=True):
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

# -------------------------------------------------------------------------------------- CRIANDO DF MOV_FINANCEIRAS - 3

    # Não pôr expander pois df não será exibido para usuário
    df_mov_financeiras = criar_df_mov_financeiras(df_movimentacoes)
    # st.write('Tabela de Movimentações Financeiras') # Comentar e manter apenas para manutenção
    # st.dataframe(df_mov_financeiras)



# ==========================================================================================================================================================================

    # -----------------------------------------------------TESTES:-------------------------------------------
    with st.expander("Teste de Cotação 1: Yahoo Finance", expanded=True):
        df_cotacao_yf = criar_df_cotacao_yf(df_mov_financeiras)
        st.dataframe(df_cotacao_yf)

    with st.expander("Teste de Cotação 2: Trading View B3", expanded=True):
        df_cotacao_tvb3 = criar_df_cotacao_tvb3(df_mov_financeiras)
        st.dataframe(df_cotacao_tvb3)

    with st.expander("Teste de Cotação 3: Status Invest", expanded=True):
        df_cotacao_statusinvest = criar_df_cotacao_statusinvest(df_mov_financeiras)
        st.dataframe(df_cotacao_statusinvest)

# ************************************************************************************************************
# próximos passos:

# pegar a cotação em Status Invest para ter uma 2a opção caso dê erro na 1a.




# -----------------------------
# Quando for criar o df_mov_financeiras, talvez seja melhor usar a mesma fx que cria o df_mov, mas já com o nome df_mov_fin,
# pois assim é um jeito de o df_mov_fin ser totalmente independente do df_mov. Se for mesmo fazer isso, depois por obs na fx:
# informando que ela é usada como ponto de partida dos dfs mov e mov_fin. Mas antes tentar pegar o df_mov pronto mesmo pois
# acho que dá


# Informar que dados estão seguros


