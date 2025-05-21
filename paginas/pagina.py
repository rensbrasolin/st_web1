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

from funcoes.pos_atual.fx_df_mov_financeiras import criar_df_mov_financeiras
from funcoes.pos_atual.fx_df_pos_atual import criar_df_pos_atual



st.title("📊 Invest View")
st.write(" #### 🔎 Análise do Extrato de Movimentações da B3")

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

# ------------------------------------------------------------------------------------------- CRIANDO DF_POS_ATUAL - 4

    with st.expander("📈 Posição Atual", expanded=True):  # Comentar e manter apenas para manutenção
        with st.container(border=True):
            df_pos_atual = criar_df_pos_atual(df_mov_financeiras)
            st.dataframe(df_pos_atual.round(2))




# ==========================================================================================================================================================================

    # -----------------------------------------------------TESTES:------------------------------------------






# ************************************************************************************************************
# próximos passos:

# a questão da TIR: dificil
# criar fx ja no arquivo mas ir exibindo df dela na pagina até ficar pronto.
# O problema da TIr é com o total/indicador, não com a tabela. O cartão é criado dentro da p´ropria função, e isso não deixa filtrar por ativo.
# Ir fazendo aos poucos para ir sentindo se vai dar muito rtrabalaho ou não.
# Primeiro de tudo, fazer a tabela funcionar, depois ver o o total

# Precisa ver a questão dos totais: médio


# -----------------------------


