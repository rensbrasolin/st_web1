import streamlit as st
import pandas as pd
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
from funcoes.pos_atual.fx_df_pos_atual import (
    criar_df_pos_atual,
    criar_filtro_tipo_df_pos_atual,
    criar_medidas_df_pos_atual,
    exibir_medidas_df_pos_atual
)

# Especialmente calculada aqui para sofrer influencia dos filtros
from funcoes.pos_atual.colunas.col_consolidadas.fx_col_consolidadas_tir import criar_tir_total_df_pos_atual



st.title("📊 Minha Carteira - Análise do Extrato de Movimentações da B3")


# ------------------------------------------------------------------------------------------------- CARREGANDO ARQ - 1


with st.expander("📂 Carregamento dos dados", expanded=True): # Comentar e manter apenas para manutenção
    st.metric(label="ℹ️", value="", help="""
    # Carregamento dos dados\n
    Como baixar o Extrato de Movimentações?
    - Acesse o site da B3: https://www.b3.com.br/pt_br/para-voce
    - No site da B3, clique em 'Área do Investidor', ou acesse direto: https://www.investidor.b3.com.br/
        - Faça login ou crie seu acesso
    - Dentro da 'Área do Investidor', no menu principal, clique em "Extratos"
    - Em "Extratos", clique em "Movimentação"
    - Em "Movimentação", clique e abra o filtro
    - No filtro:
        - Escolha Data Inicial e Data Final para selecionar o período desejado
            - Para o correto funcionamento da aplicação, é obrigatório que o extrato contemple todo o período da carteira
        - Na seção "Tipo de Investimento", selecione apenas Ações, ETFs e FIIs
        - Clique em 'Filtrar'
    - E por fim, clique em 'Baixar' e salve o arquivo em seu PC
        """)

    # with st.container(border=True):
        # Usuário carregará 1 ou mais arquivos de extrato de movimentação
    arquivos = st.file_uploader("Carregue aqui o seu Extrato de Movimentações",
                                    type=["xlsx", "xls"], accept_multiple_files=True)

# ------------------------------------------------------------------------------------------------- CRIANDO DF MOV - 2a

# If para não aparecer um df vazio de início.
# Todu o resto do cód tem que estar dentro desse if, obrigatoriamente. Sem df_mov não há app.
if arquivos:

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

# ------------------------------------------------------------------------------------------------- EXIBINDO DF MOV - 2b
#     Expanded para Inicar aberto para carregar aggrid corretamente
    with st.expander("📃 Extrato de Movimentações", expanded=True):
        st.metric(label="ℹ️", value="", help="""
        # Extrato de Movimentações
        - Aplique filtros na tabela para que os indicadores abaixo se ajustem
        """)
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

# ------------------------------------------------------------------------------------------- CRIANDO DF_POS_ATUAL - 4a

    with st.expander("🔎 Posição Atual", expanded=True):
        st.metric(label="ℹ️", value="", help="""
        # Posição Atual
        - Visualize a Posição Atual da Carteira como um todo, ou filtre por ativo
        - Indicadores, tabela, e gráficos abaixo, serão ajustados pelo filtro
        """)


        # Criado logo antes do filtro e exibido só após os indicadores
        df_pos_atual = criar_df_pos_atual(df_mov_financeiras)

# ------------------------------------------------------------------------------------ CRIANDO FILTRO DF_POS_ATUAL - 4b

        with st.container(border=True):
            df_pos_atual = criar_filtro_tipo_df_pos_atual(df_pos_atual)


# -------------------------------------------------------------------------------- INDICADORES/TOTAIS DF_POS_ATUAL - 4c

        (  # FX retorna todas as variáveis de totais, menor TIR
            qtd_ativos_total_df_pos_atual, # Essa até faz sentido mostrar.
            qtd_tipos_total_df_pos_atual, # # Não faz sentido, já que df pode ser filtrado.
            qtd_total_df_pos_atual,  # Não será usada provavelmente

            custo_medio_total_df_pos_atual,
            remuneracoes_total_df_pos_atual,
            res_vendas_total_df_pos_atual,
            patrimonio_atual_total_df_pos_atual,
            variacao_percentual_total_df_pos_atual,
            variacao_absoluta_total_df_pos_atual,
            yield_total_df_pos_atual,
            performance_absoluta_total_df_pos_atual,
            performance_percentual_total_df_pos_atual
        ) = criar_medidas_df_pos_atual(df_pos_atual)

        # Especialmente calculada aqui para sofrer influencia dos filtros do df_pos_atual
        tir_total_df_pos_atual = criar_tir_total_df_pos_atual(
            df_pos_atual, df_mov_financeiras, patrimonio_atual_total_df_pos_atual)


# ---------------------------------------- EXIBINDO INDICADORES/TOTAIS DF_POS_ATUAL
#         with st.container(border=True):  # Tirei o container para ter espaço
        exibir_medidas_df_pos_atual(
            qtd_ativos_total_df_pos_atual, # Essa até faz sentido mostrar.
            qtd_tipos_total_df_pos_atual, # Não faz muito sentido, já que df pode ser filtrado.
            qtd_total_df_pos_atual,  # Não será usada provavelmente

            custo_medio_total_df_pos_atual,
            remuneracoes_total_df_pos_atual,
            res_vendas_total_df_pos_atual,
            patrimonio_atual_total_df_pos_atual,
            variacao_percentual_total_df_pos_atual,
            variacao_absoluta_total_df_pos_atual,
            yield_total_df_pos_atual,
            performance_absoluta_total_df_pos_atual,
            performance_percentual_total_df_pos_atual,
            tir_total_df_pos_atual,
        )

# ------------------------------------------------------------------------------------------- EXIBINDO DF_POS_ATUAL - 4d

        with st.container(border=True):
            st.dataframe(df_pos_atual.round(2))
            # st.dataframe(df_mov_financeiras.round(2))





# ==========================================================================================================================================================================

    # -----------------------------------------------------TESTES:------------------------------------------






# ************************************************************************************************************
# próximos passos:



# VER SE TEM MAIS ALGUM AJUSTE:
# Talvez um discalmner inicial
# subir e testar

# imagem do ativo, provavelmnete só com aggrid









# -----------------------------





